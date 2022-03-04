# ShiftyFace

A simple python module for generating random images with rarity level you dictate and assets you provide. The primary use case being the generation of images for NFTs or other nefarious endeavors.

## Installation

~~~
pip install shiftyface
~~~

## Usage and Settings

### General Concept

Shiftyface works be reading a traits json file (format below) that you provide, and builds images using layered assets you or a designer create.

By default it expects a 'traits' folder at your application's route. This folder is expected to contain a directory called assets that contains your layered images in respective category directories.

For example, if you wish to create a series of images representing fatigued primates in a nautical  setting, each with their own semi-unique eyes, mouths, hats etc, you would create a directory at the following path: ./traits/assets.
Inside this directory you would have addition directories like 'eyes', 'hats', etc, each containing the assets to be randomized when images are created.

You would then create a file called "traits.json" inside the traits director that identifies each trait and their choices (as image names), as well as the corresponding rarity assigned to each.

### Example Traits File

here is an example traits.json file that would be in the ./traits folder:

~~~
{
  "order": ["face", "mouth", "eyes","nose", "hair", "ears", "access"],
  "rarity": {
    "face": {
      "choices": ["face1.png", "face2.png"],
      "weights": [40, 60]
    },
    "mouth": {
      "choices": ["m1.png", "m2.png", "m3.png", "m4.png", "m5.png"],
      "weights": [30, 25, 20, 16, 10]
    },
    "eyes": {
      "choices": ["eyes1.png","eyes2.png","eyes3.png","eyes4.png","eyes5.png"],
      "weights": [40, 30, 20, 7, 3]
    },
    "nose": {
      "choices": ["n1.png", "n2.png"],
      "weights": [65, 35]
    },
     "hair": {
      "choices": ["hair1", "hair2", "hair3", "hair4", "hair5", "hair6", "hair7", "hair8", "hair9", "hair10"],
      "weights": [15, 10, 10, 10, 10, 10, 10, 10, 10, 5]
    },

    "ears": {
      "choices": ["ears1.png", "ears2.png", "ears3.png", "ears4.png"],
      "weights": [45, 25, 20, 10]
    },
    "access": {
      "choices": ["acc1.png", "acc2.png"],
      "weights": [70, 30]
    }


  }
}
~~~

