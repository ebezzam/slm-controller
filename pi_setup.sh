#!/bin/sh

# OS requirements
sudo apt-get -y install libatlas-base-dev
sudo apt-get -y install ttf-dejavu


# create Python 3 virtual environment
python3 -m pip install --user virtualenv
virtualenv -p python3 photonics_env
source photonics_env/bin/activate


# install dependencies
pip install adafruit-circuitpython-rgb-display
pip install pillow==5.4.1
pip install numpy==1.16.2
pip install click
