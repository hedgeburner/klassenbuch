#!/bin/bash

# use a virtual python environment
virtualenv env

env/bin/python setup.py develop

env/bin/pserve development.ini --reload