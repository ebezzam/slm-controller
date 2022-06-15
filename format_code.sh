#!/bin/sh

black *.py -l 100
black examples/*.py -l 100
black slm_controller/**/*.py -l 100
black tests/*.py -l 100
