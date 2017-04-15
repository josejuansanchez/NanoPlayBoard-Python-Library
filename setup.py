from setuptools import setup

setup(name='nanoplayboard',
      version='0.0.1',
      description='A Python Library for NanoPlayBoard Firmata',
      keywords=['NanoPlayBoard', 'Arduino', 'Firmata'],
      url='https://github.com/josejuansanchez/NanoPlayBoard-Python-Library',
      author='Antonio Morales and Jose Juan Sanchez',
      author_email='josejuan.sanchez@gmail.com',
      license='GNU General Public License v3 (GPLv3)',
      install_requires=['pymata_aio'],
      packages=['nanoplayboard'],
      zip_safe=False)