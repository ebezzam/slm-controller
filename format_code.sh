#!/bin/bash

# Apparently black formats differently in Linux and Windows: https://github.com/psf/black/issues/3037#issuecomment-1110607036

black -l 100 *.py
black -l 100 examples/*.py
black -l 100 slm_controller/*.py
black -l 100 slm_controller/**/*.py
