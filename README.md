# SLM controller

Scripts and modules to control displays with Python.

Note that our convention for dimension order is (# channels x height x width).

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

```sh
source photonics_env/bin/activate
```
You can exit the virtual environment by running `deactivate`.

To display a randomly generated grayscale image, run the following command:

```sh
python examples/rgb_display.py
```

For a randomly generated RGB image:

```sh
python examples/rgb_display.py --rgb
```

For an image, you can pass the file path:

```sh
python examples/rgb_display.py --file_path examples/blinka.jpg
```
The original image will be rescaled and cropped to match the original aspect ratio.
