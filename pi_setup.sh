#!/bin/sh

# OS requirements
sudo apt-get -y install libatlas-base-dev
sudo apt-get -y install ttf-dejavu


# create Python 3 virtual environment
python3 -m pip install --user virtualenv
virtualenv -p python3 photonics_env
source photonics_env/bin/activate


# install dependencies
pip install click
pip install -e .
