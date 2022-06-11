#!/bin/sh

black *.py -l 100

black examples_controller/*.py -l 100
black examples_design/*.py -l 100

black slm_controller/**/*.py -l 100
black slm_design/**/*.py -l 100

black tests/*.py -l 100
