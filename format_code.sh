#!/bin/bash

black -l 100 --include $(find -name "*.py")

# black *.py -l 100
# black examples/*.py -l 100
# black slm_controller/*.py -l 100
# black slm_controller/**/*.py -l 100
# black tests/*.py -l 100

# TODO black formats differently in Linux and Windows...
# TODO better version for matching all files and all files in subdirectories
