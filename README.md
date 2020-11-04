# SLM controller

Scripts and modules to control displays with Python.

## Installation

The target platform is a Raspberry Pi. After cloning this repository, you can
install the necessary dependencies by running the following script:

```sh
./pi_setup.sh
```

The script will:
1. Install OS dependencies.
2. Create a Python3 virtual environment called `photonics_env`.
3. Install Python dependencies in the virtual environment.

## Example scripts

Activate the virtual environment:

```python
source photonics_env/bin/activate
```
You can exit the virtual environment by running `deactivate`.

For displaying an image, check out the following script:

```python
python3 rgb_display_image.py
```

For displaying a numpy array, check out the following script:

```python
python3 rgb_display_numpy.py
```
