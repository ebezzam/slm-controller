#!/bin/bash

black -l 100 *.py
black -l 100 examples/*.py
black -l 100 slm_controller/*.py
black -l 100 slm_controller/**/*.py
black -l 100 tests/*.py

# TODO black formats differently in Linux and Windows...
# TODO better version for matching all files and all files in subdirectories
