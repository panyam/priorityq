"""
PriorityQ
---------

PriorityQ is a library for managing a priority queue (PQ) with a cleaner API to enable custom comparators, 
finding references to values efficiently (in constant time) and deleting values from the PQ.   This was 
developed because the current heapq module (in python's standard library) does not provide an efficient
find operation (it is O(n)) and has no easy way to deleting an element and ensuring the heap invariant
afterwards.

Features
````````

* O(1) finding of elements
* Deletion of elements possible (in O(log n)).
* Adjusting of the priority of an element without requiring a deletion followed by an insertion.
* Opaque handles to elements that can be used to reference to the same item again.
* Duplicate elements allowed.
* Custom comparator function can be passed to the PQ itself instead of needing to implement __cmp__.

It is simple to use
```````````````````

To create a PQ simply do:

.. code:: python

    # A simple object with a comparator
    class Item(object):
        def __init__(self, value):
            self.value = value
        def __cmp__(self, another):
            return cmp(self.value, another.value)

    from priorityq import PQ
    pq = PQ()
    pq.heapify([Item(r) for r in [1, 10, 2, 20, 4, 7, 9, 3, 5, 6]])

    print list(pq)

    # Should print:
    # 1 2 3 4 5 6 7 9 10 20

    handle_10 = pq.find(25)   #   Happens in O(1)

    handle_10.value = 12      #   Modify its value - O(log n)
    pq.adjust(handle_10)      #   Indicate to the heap to reprioritise/adjust it

    print list(pq)

    # Should print:
    # 1 2 3 4 5 6 7 9 20 25

    handle_10.value = 10      #   Modify its value using the same opaque pointer as before
    pq.adjust(handle_10)      #   Indicate to the heap to reprioritise/adjust it

    print list(pq)

    # Should print:
    # 1 2 3 4 5 6 7 9 10 20

Links
`````
* `Documentation Wiki <https://github.com/panyam/priorityq/wiki>`_
* `Website <https://github.com/panyam/priorityq>`_
"""

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


with open('priorityq/__init__.py', 'rb') as f:
    _version_re = re.compile(r'__version__\s+=\s+(.*)')
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

# for scheme in INSTALL_SCHEMES.values(): scheme['data']=scheme['purelib']

print "=" * 80
print "Packages: ", find_packages(exclude=EXCLUDE_FROM_PACKAGES)
print "=" * 80

setup(name="priorityq",
      version=version,
      requires = [ ],
      description="A clean priority queue library with several types and utility helpers.",
      author="Sri Panyam",
      author_email="sri.panyam@gmail.com",
      url="https://github.com/panyam/priorityq",
      package_data = {
          'priorityq': [
              "data/templates/backends/java/*",
              "data/templates/transformers/java/*"
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
