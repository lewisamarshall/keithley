from setuptools import setup, find_packages

setup(name='keithley',
      version='0.1.0',
      author='Lewis A. Marshall',
      author_email='lewis.a.marshall@gmail.com',
      url='https://github.com/lewisamarshall/keithley',
      use_2to3=True,
      description='A Python package for analyzing Purigen data files.',
      packages=find_packages(),
      requires=['serial'],
      package_data={}
      )
