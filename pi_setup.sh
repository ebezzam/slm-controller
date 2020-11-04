#!/usr/bin/env bash

# create Python 3 virtual environment
python -m pip install --user virtualenv
virtualenv -p python3 venv3
source venv3/bin/activate

# OS requirements
sudo apt-get -y install libatlas-base-dev
sudo apt-get -y install ttf-dejavu

# install dependencies
pip install adafruit-circuitpython-rgb-display
pip install pillow==5.4.1
pip install numpy==1.16.2
