from setuptools import setup, find_packages


setup(
    name='shiftyface',
    version='0.1',
    license='MIT',
    author="Paul Thompson",
    author_email='pt@sevenelm.com',
    packages=find_packages('shifty_face'),
    package_dir={'': 'shifty_face'},
    url='https://github.com/rpupkin77/shiftyface',
    keywords='nft, rarity, image generation, eth, collection generator',
    install_requires=[
          'Pillow',
      ],

)