# slm-controller

Scripts and modules to control SLMs with Python.

Note that our convention for dimension order is (channels, height, width).

## Overview

The main goal of the project is to provided an abstraction level for different
SLM devices.

## Installation

<!-- TODO Still only raspberry pi? -->

The target platform is a Raspberry Pi. After cloning this repository, you can
install the necessary dependencies by running the following script:

```sh
./pi_setup.sh
```

The script will:

1. Install OS dependencies.
2. Create a Python3 virtual environment called `slm_controller_env`.
3. Install Python dependencies in the virtual environment.

But the software needed for [Holoeye LC
2012](https://holoeye.com/lc-2012-spatial-light-modulator/) `is only supported on Windows operating systems!`

### No Raspberry Pi?

You can still try out some features of this library by running:

```sh
pip install -e .[dev]
```

You won't be able to run any examples that use the physical SLMs.

## Manual installation needed for enabling some features

For the using the [Holoeye LC
2012](https://holoeye.com/lc-2012-spatial-light-modulator/) SLM implemented in the
project you will need to manually download Holoeye's [SLM Display
SDK](https://customers.holoeye.com/slm-display-sdk-v3-0-for-python-windows/) and
install it. `Only Windows operating systems are supported currently by the SDK!` Just
follow the installation instructions. The script located at
`slm_controller/holoeye` is then determining the specific path to your installation of the
SDK automatically whenever it is needed.

## Example scripts

In `examples` are various example scripts to control an RGB and a monochrome
(binary) SLMs by
Adafruit, a Nokia SLM and Holoeye's SLM.

First, activate the virtual environment:

```sh
source slm_controller_env/bin/activate
```

You can exit the virtual environment by running `deactivate`.

### RGB SLM

To display a randomly generated grayscale image:

```sh
python examples/rgb_slm.py
```

For a randomly generated RGB image:

```sh
python examples/rgb_slm.py --rgb
```

For an image, you can pass the file path:

```sh
python examples/rgb_slm.py --fp images/blinka.jpg
```

The original image will be rescaled and cropped to match the original aspect ratio.

### Monochrome SLM

To display a randomly generated monochrome image:

```sh
python examples/binary_slm.py
```

For an image, you can pass the file path:

```sh
python examples/binary_slm.py --file_path images/blinka.jpg
```

The original image will be rescaled and cropped to match the original aspect ratio.

With the following command, a simple reshape will be performed which can distort the original image.

```sh
python examples/binary_slm.py --file_path images/blinka.jpg --not_original_ratio
```

### Nokia SLM

<!-- TODO add documentation for nokia slm example -->

```sh
>> python examples/nokia_slm.py --help
Usage: nokia_slm.py [OPTIONS]

Options:
  --file_path TEXT
  --not_original_ratio
  --help                Show this message and exit.
```

### Holoeye SLM

This script is an example of how to use the Holoeye LC 2012 SLM. It does simply
create checkerboard phase map and sends it the the SLM. The checkerboard was
chosen because its resulting interference pattern at the target plane is highly
different from the one produces by the blank SLM.

```sh
>> python examples/holoeye_slm.py --help
Usage: holoeye_slm.py [OPTIONS]

Options:
  --show_time FLOAT  Time to show the pattern on the SLM.
  --help             Show this message and exit.
```

## Adding new SLM

1. Add configuration in `slm_controller/hardware.py:slm_devices`.
2. Create class in `slm_controller/slm.py`.
3. Add to factory method `create_slm` in `slm_controller/slm.py`.
