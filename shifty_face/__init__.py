import csv
import json
import logging
import os
import random
import shutil

from PIL import Image

from shifty_face.example.settings import TRAITS_SETTINGS

# configure logging level
logging.basicConfig(level=logging.INFO)


class ShiftyFace(object):

    def __init__(self, count, **kwargs):

        """
        :param count: the number of billion dollar NFTs to create
        """

        self.dry_run = kwargs.get("dry_run", False)

        # get the current working directory for pathing
        cwd = os.getcwd()

        # set up directory attributes from settings
        traits_directory = TRAITS_SETTINGS.get("base_directory", "traits")
        traits_file = TRAITS_SETTINGS.get("traits_file", "traits.json")
        assets_directory = TRAITS_SETTINGS.get("assets_directory", "assets")
        output_directory = TRAITS_SETTINGS.get("output_directory", "output")

        # open the traits file and setup image building attributes
        with open(f"{cwd}/{traits_directory}/{traits_file}", "r") as traits_file:
            traits_json = traits_file.read()
            traits = json.loads(traits_json)

        # instantiate class attributes for source and destination dirs
        self.src_dir = f"{cwd}/{traits_directory}/{assets_directory}"
        self.output_dir = f"{cwd}/{output_directory}"

        # delete the output directory if it exists, we need to ensure that it is empty to start
        if os.path.exists(self.output_dir) and os.path.isdir(self.output_dir):
            shutil.rmtree(self.output_dir)

        # now, recreate it Lolz
        os.makedirs(self.output_dir)

        # instantiate class attributes pertaining to the asset traits
        self.rarity = traits['rarity']
        self.trait_count = len(traits['order'])
        self.trait_keys = list(traits['order'])

        # instantiate class variables for tracking images as they are created.
        self.count = count
        self.generated_images = []
        self.unique_images = []
        self.ad = 0
        self.n = 0
        self.trait_stats = {}

        # generate a dictionary for tracing rarity
        for i, v in self.rarity.items():
            self.trait_stats[i] = {}
            for c in v['choices']:
                self.trait_stats[i][c] = 0

    def _generate_images(self):
        """
        Generates images based on randomly generated asset collections based on "rarity"
        :return: None
        """
        for item in self.unique_images:
            asset_holder = []
            for trait, image in item.items():
                try:
                    asset_holder.append(Image.open(f'{self.src_dir}/{trait}/{image}').convert('RGBA'))

                except FileNotFoundError:
                    logging.debug("Passable key error - not a valid trait, skipping")
                except Exception as e:
                    logging.warning(f"Error counting traits for a image set: {e.__str__()}")

            # Create each composite
            composite = {}
            a = 0
            for asset in asset_holder:
                if a == 0:
                    composite[str(a)] = Image.alpha_composite(asset_holder[a], asset_holder[a + 1])
                else:
                    composite[str(a)] = Image.alpha_composite(composite[str(a - 1)], asset_holder[a])
                a += 1
            """
            com1 = Image.alpha_composite(asset_holder[0], asset_holder[1])
            com2 = Image.alpha_composite(com1, asset_holder[2])
            com3 = Image.alpha_composite(com2, asset_holder[3])
            com4 = Image.alpha_composite(com3, asset_holder[4])
            """

            # Convert to RGB
            rgb_image = composite[str(a - 1)].convert('RGB')
            file_name = str(item["token_id"]) + "_" + str(item["rarity_score"]) + ".png"

            rgb_image.save(f"{self.output_dir}/" + file_name)

    def _count_traits(self):
        """
        Utility function - counts the number of traits used
        :return: None
        """
        for i in self.unique_images:
            for k, v in i.items():
                try:
                    self.trait_stats[k][v] += 1
                except KeyError:
                    logging.debug("passable key error - not a valid trait, skipping")
                except Exception as e:
                    logging.warning(f"Error counting traits for a image set: {e}")

    def _validate_uniqueness(self):
        """
        Confirms each "image" definition is unique, if so, adds to the final set for processing
        :return:
        """
        x = 0
        for i in self.generated_images:

            if i not in self.unique_images:
                i['token_id'] = x
                self.unique_images.append(i)
                x += 1

    def _get_image_rarity(self, image):
        """
        Gnerates a rarity score for an image definition based on traits
        :param image: dictionary representing an iag eto be generated
        :return: float: the image's rarity based upon randomly chosen traits
        """
        # start score at 100 and decrease
        rarity_score = 100

        for k, v in image.items():
            if k in self.trait_keys:
                # rarity score 100 - (each trait rarity / number of traits), division is to get it relative to 100.
                # rarity can never be 100, but it also will never be below 0
                rarity_score -= (self.rarity[k]['weights'][self.rarity[k]['choices'].index(v)] / self.trait_count)

        return round(rarity_score, 1)

    def _create_image(self):
        """
        Creates image definitions based on supplied traits
        :return: dict: dictionary representing traits that will make up the image
        """

        new_image = {}

        for i in self.trait_keys:
            try:
                new_image[i] = random.choices(self.rarity[i]['choices'], self.rarity[i]['weights'])[0]
            except ValueError as ve:
                logging.error(f"Error Generating the image from traits (trait: {i}): {ve}")
                exit()

        # if the image already exists, run again, otherwise return the image trait dict
        if new_image in self.generated_images:
            self.ad += 1
            return self._create_image()
        else:
            self.n += 1
            new_image['rarity_score'] = self._get_image_rarity(new_image)
            return new_image

    def _generate_inventory_file(self):
        """
        creates a csv in the output folder with details on the generated files
        :return:
        """

        # create the buffer for a csv outputfile
        first = True
        buffer = []

        for item in self.unique_images:
            # get the keys and values (as lists) for each iteration
            the_keys = list(item.keys())
            the_values = list(item.values())

            # reverse them to ensure id and rarity are first
            the_keys.reverse()
            the_values.reverse()

            # if first, use the keys to create the column names, else just append vals
            if first:
                buffer.append(the_keys)
                buffer.append(the_values)
                first = False
            else:
                buffer.append(the_values)

        with open(f'{self.output_dir}/inventory.csv', 'w') as inventory_file:
            inventory_writer = csv.writer(inventory_file)
            inventory_writer.writerows(buffer)

    def generate(self):
        """
        kicks off image generation process, call this method from your main program
        :return: None
        """
        logging.info("Start generation of images...")

        logging.info("Creating image definitions...")
        # generate the unique image definitions
        for i in range(self.count):
            self.generated_images.append(self._create_image())

        # now, validate uniqueness
        logging.info("Validating uniqueness...")
        self._validate_uniqueness()

        # count traits
        logging.info("Tallying trait usage...")
        self._count_traits()

        # generate future $$ nfts ;)
        # don't generate if dry run
        if not self.dry_run:
            logging.info("Generating images - may take a moment...")
            self._generate_images()

        # generate inventory file
        logging.debug("Creating image creation log (inventory.csv) in output directory...")
        self._generate_inventory_file()

        # send output to console
        if not self.dry_run:
            logging.info("Image Generation Complete.")
        else:
            logging.info("Dry run complete, check output folder for inventory.csv to see what "
                         "would have been generated.")
