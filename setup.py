import os

from pip.req import parse_requirements
from setuptools import setup, find_packages

install_reqs = parse_requirements('requirements.txt', session=False)
reqs = [str(ir.req) for ir in install_reqs]


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name="emailme",
      version="0.2.0",
      author="Eric J. Ma",
      author_email="ericmajinglong@gmail.com",
      description=("Super simple self-emailing."),
      license="MIT",
      packages=find_packages(),
      keywords="email",
      url="http://github.com/ericmjl/emailme",
      package_data={'': ['README.md']},
      install_requires=reqs,
      long_description=read('README.md'),
      entry_points={'console_scripts': ['emailme=emailme:cli']}
      )
