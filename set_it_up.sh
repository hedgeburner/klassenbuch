#!/bin/bash

# use a virtual python environment
virtualenv env

#env/bin/pip install foo bar

env/bin/pip install pyramid

env/bin/pcreate -t alchemy klassenbuch

env/bin/pserve development.ini --reload