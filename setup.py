# To update the pypi package:
# You need an account at pypi.org and to be added to the project
#
# increment version
# remove egg info, dist
# python setup.py sdist
# python setup.py bdist_wheel --universal
# twine upload dist/*
#
# Local, editable install:
# pip install -e ~/Github/py2mappr
#

from setuptools import setup
from setuptools import find_packages

setup(name='py2mappr',
      version='0.1.5',
      description='py2mappr',
      long_description="py2mappr",
      url='https://github.com/vibrant-data-labs/py2mappr',
      author='ericberlow',
      author_email='ericberlow@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'numpy',
          'pandas',
          'tag2network @ git+https://github.com/vibrant-data-labs/Tag2Network',
          'markdown',
          'markdown3-newtab',
          "jsonschema",
          "requests"
      ],
      include_package_data=True,
      zip_safe=False)
