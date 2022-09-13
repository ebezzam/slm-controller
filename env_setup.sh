#!/bin/bash
# OS requirements
if cat /proc/device-tree/model | grep -q 'Raspberry'; then
    sudo apt-get -y install libatlas-base-dev
    sudo apt-get -y install ttf-dejavu
fi

# create Python 3 virtual environment
python3 -m pip install --user virtualenv
virtualenv -p python3 slm_controller_env
source slm_controller_env/bin/activate

# install package
pip install -e .
