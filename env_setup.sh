#!/bin/bash
# OS requirements
sudo apt-get -y install libatlas-base-dev # TODO only on Raspberry Pi, two scripts
sudo apt-get -y install ttf-dejavu

# create Python 3 virtual environment
python3 -m pip install --user virtualenv
virtualenv -p python3 slm_controller_env
source slm_controller_env/bin/activate

# install package
pip install -e .
