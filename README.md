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

To display a randomly generated grayscale image, run the following command:

```python
python example.py
```

For a randomly generated RBG image:

```python
python example.py --rgb
```

For an image, you can pass the file path:

```python
python example.py --file_path blinka.jpg
```
