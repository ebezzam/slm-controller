# SLM controller

Scripts and modules to control displays with Python.

## Installation

The target platform is a Raspberry Pi. After cloning this repository, you can
install the necessary dependencies by running the following script:

```bash
./pi_setup.sh
```

The script will:
1. Install OS dependencies.
2. Create a Python 3 virtual environment called `venv3`.
3. Install Python dependencies in the virtual environment.

## Example scripts

Activate the virtual environment:

```python
source venv3/bin/activate
```
You can exit the virtual environment by running `deactivate`.

For displaying an image, check out the following script:

```python
python rgb_display_image.py
```

For displaying a numpy array, check out the following script:

```python
python rgb_display_numpy.py
```