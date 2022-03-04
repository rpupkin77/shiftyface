from setuptools import setup, find_packages


setup(
    name='shiftyface',
    long_description='A simple python module for generating random images with rarity level you dictate and assets you '
                     'provide. The primary use case being the generation of images which can be turned into NFTs.',
    version='0.4.1',
    license='MIT',
    author="Paul Thompson",
    author_email='pt@sevenelm.com',
    packages=['shifty_face'],
    url='https://github.com/rpupkin77/shiftyface',
    keywords='nft, rarity, image generation, eth, collection generator',
    install_requires=[
          'Pillow',
      ],

)