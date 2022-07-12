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
      version='0.0.1',
      description='py2mappr',
      long_description="py2mappr",
      url='https://github.com/ericberlow/py2mappr',
      author='ericberlow',
      author_email='ericberlow@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'numpy', 'pandas', 'pyyaml'
      ],
      zip_safe=False)
