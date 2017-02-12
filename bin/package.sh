#!/bin/sh

rm -Rf build dist priorityq.egg-info
python setup.py sdist
python setup.py bdist_wheel --universal
rm -Rf priorityq.egg-info
