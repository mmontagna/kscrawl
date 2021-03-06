import os
from setuptools import setup, find_packages

dir_path = os.path.dirname(os.path.realpath(__file__))

VERSION = open(os.path.join(dir_path, 'VERSION')).read()

setup(
  name = 'kscrawl',
  packages = find_packages(),
  version = VERSION,
  description = '''
  
  ''',
  author_email = 'marcojoemontagna@gmail.com',
  url = 'https://github.com/mmontagna/kscrawl',
  keywords = [],
  classifiers=(
  ),
  data_files = [('', ['VERSION', 'README.md'])],
  include_package_data=True,
  python_requires=">=2.7",
  install_requires=[
    "attrdict==2.0.0",
    "beautifulsoup4==4.4.1",
    "boto3>=1.2.4",
    "botocore>=1.3.29",
    "chardet==2.3.0",
    "coverage==4.0.3",
    "dill==0.2.5",
    "docutils==0.12",
    "funcsigs==0.4",
    "futures==3.0.5",
    "jmespath==0.9.0",
    "mock==1.3.0",
    "nltk==3.1",
    "numpy==1.10.4",
    "pbr==1.8.1",
    "python-dateutil==2.4.2",
    "redis==2.10.5",
    "scikit-learn==0.17.1",
    "scipy==0.17.0",
    "six==1.10.0",
    "urlnorm==1.1.3",
    "virtualenv==14.0.6",
    "wheel==0.29.0",
    "selenium==2.52.0"
  ],
  extras_require={
  },
  entry_points = {
  },
)
