import re
from setuptools import setup

version = re.search(
  '^__version__\s*=\s*"(.*)"',
  open('xml2graph/xml2graph.py').read(),
  re.M
  ).group(1)

with open("README.md", "rb") as f:
  long_descr = f.read().decode("utf-8")
    
setup(
  name="xml2graph",
  packages=["xml2graph"],
  entry_points={"console_scripts":['xml2graph=xml2graph.xml2graph:main']},
  version=version,
  description="Creates UML graphs from an xml file.",
  long_description=long_descr,
  author="Chris Geroux",
  author_email="chris.geroux@ace-net.ca",
  url="",
  test_suite='nose.collector',
  test_require=['nose'],
  include_package_data=True
  )