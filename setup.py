from __future__ import absolute_import
import os
import re
import ast
import sys
from distutils.sysconfig import get_python_lib

from setuptools import find_packages
from setuptools import setup

# Warn if we are installing over top of an existing installation. 
overlay_warning = False
if "install" in sys.argv:
    lib_paths = [get_python_lib()]
    if lib_paths[0].startswith("/usr/lib/"):
        # We have to try also with an explicit prefix of /usr/local in order to
        # catch Debian's custom user site-packages directory.
        lib_paths.append(get_python_lib(prefix="/usr/local"))
    for lib_path in lib_paths:
        existing_path = os.path.abspath(os.path.join(lib_path, "priorityq"))
        if os.path.exists(existing_path):
            # We note the need for the warning here, but present it after the
            # command is run, so it's more likely to be seen.
            overlay_warning = True
            break


# Any packages inside the priorityq source folder we dont want in the packages
EXCLUDE_FROM_PACKAGES = [ ]

# for scheme in INSTALL_SCHEMES.values(): scheme['data']=scheme['purelib']

print "=" * 80
print "Packages: ", find_packages(exclude=EXCLUDE_FROM_PACKAGES)
print "=" * 80

def get_version():
    with open('priorityq/__init__.py', 'rb') as f:
        _version_re = re.compile(r'__version__\s+=\s+(.*)')
        return str(ast.literal_eval(_version_re.search(f.read().decode('utf-8')).group(1)))

def get_description():
    return open("README.rst").read()

setup(name="priorityq",
      version=get_version(),
      requires = [ ],
      extras_require={'docs': ['Sphinx>=1.1']},
      tests_require = [ "pytest" ],
      description="A clean priority queue library with several types and utility helpers.",
      long_description=get_description(),
      author="Sri Panyam",
      author_email="sri.panyam@gmail.com",
      url="https://github.com/panyam/priorityq",
      package_data = {
          'priorityq': [
          ]
      },
      packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
      include_package_data = True,
      scripts = [],
      zip_safe = False,
      classifiers=[
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
      ]
      )

if overlay_warning:
    sys.stderr.write("""

========
WARNING!
========

You have just installed Onering over top of an existing
installation, without removing it first. Because of this,
your install may now include extraneous files from a
previous version that have since been removed from
Onering. This is known to cause a variety of problems. You
should manually remove the

%(existing_path)s

directory and re-install Onering.

""" % {"existing_path": existing_path})
