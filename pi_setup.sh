#!/bin/sh

# OS requirements
sudo apt-get -y install libatlas-base-dev
sudo apt-get -y install ttf-dejavu


# create Python 3 virtual environment
python3 -m pip install --user virtualenv
virtualenv -p python3 photonics_env
source photonics_env/bin/activate


# install dependencies
python3 -m pip install adafruit-circuitpython-rgb-display
python3 -m pip install pillow==5.4.1
python3 -m pip install numpy==1.16.2
