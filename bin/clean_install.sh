#!/bin/bash

PYTHON=`which python`
PYTHON_DIR=`dirname $PYTHON`
PYTHON_LIB_DIR=`dirname $PYTHON_DIR`
echo PYTHON=$PYTHON
echo PYTHON_DIR=$PYTHON_DIR
echo PYTHON_LIB_DIR=$PYTHON_LIB_DIR

rm -Rf $PYTHON_LIB_DIR/lib/python2.7/site-packages/priorityq*
rm -Rf build dist priorityq.egg-info
rm -Rf `find ./ | grep "\.pyc#"`
python setup.py install -f 
rm -Rf build dist priorityq.egg-info
