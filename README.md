# slm-controller

Scripts and modules to control spatial light modulators (SLMs) using Python.

Note that our convention for dimension order is (channels, height, width).

- [slm-controller](#slm-controller)
  - [Installation](#installation)
    - [No Raspberry Pi for the Adafruit and Nokia SLMs?](#no-raspberry-pi-for-the-adafruit-and-nokia-slms)
    - [Holoeye SLM installation](#holoeye-slm-installation)
      - [Manual installation for Holoeye SLM](#manual-installation-for-holoeye-slm)
  - [Example scripts](#example-scripts)
    - [Adafruit SLM](#adafruit-slm)
    - [Nokia SLM](#nokia-slm)
    - [Holoeye SLM](#holoeye-slm)
  - [Adding a new SLM](#adding-a-new-slm)

The main goal of this repository is to provide a common API for different
display devices, allowing them to be used interchangeably for different applications.

Generally speaking there are two different kinds of SLMs depending on the property of the wavefront that one wishes to modulator: amplitude and phase. Note that there do exist SLMs that are able to modulate both. Currently the
project supports three different SLM devices.

Amplitude SLMs:

(Note that the amplitude SLMs below are obtained by isolating the LCD layer of off-the-shelf components.)

- [Adafruit 1.8" TFT LCD](https://learn.adafruit.com/1-8-tft-display/overview) (RGB)
- [Nokia 5110 LCD](https://learn.adafruit.com/nokia-5110-3310-monochrome-lcd) (Monochrome)

<!-- TODO Holoeye actually can do both via polarization modulation and combination with polarizer/analyzer -->

Phase SLMs:

- [Holoeye LC 2012](https://holoeye.com/lc-2012-spatial-light-modulator/)

Note that if anything goes wrong with the communication with those devices, the
phase maps are simply plotted to the screen using `matplotlib` instead of being
shown on the devices themselves.

## Installation

The supported platforms for the different SLMs are summarized below:

- Adafruit 1.8" TFT LCD: Raspberry Pi
- Nokia 5110 LCD: Raspberry Pi
- Holoeye LC 2012: Windows

After cloning this repository, you can install the necessary dependencies by
running the following script:

```sh
./env_setup.sh
```

The script will:

1. Install OS dependencies.
2. Create a Python3 virtual environment called `.slm_controller_env`.
3. Install Python dependencies in the virtual environment.

If you plan to use this code base more in depth you can install additional
dependencies intended for developing while the virtual environment is activated.

```sh
source .slm_controller_env/bin/activate
# pip install -e .[dev] #TODO does not work, dev not found
pip install click pytest black
```

### No Raspberry Pi for the Adafruit and Nokia SLMs?

You can still try out some features of this library! You won't be able to run
any example programs on the physical SLMs but the results will be plotted to
your screen instead, as mentioned earlier.

### Holoeye SLM installation

The SDK needed for [Holoeye LC
2012](https://holoeye.com/lc-2012-spatial-light-modulator/) `is only supported on Windows operating systems!` Hence using a Raspberry Pi directly is not currently supported, and a device with a live Windows instance is needed to use the Holoeye SLM. In the
future we will check if Windows running inside a container on a Raspberry Pi is
a possibility.

<!-- TODO check windows in a container -->

Additionally, you need to perform some manual installation steps, explained in the
next section, after having run the installation script above.

#### Manual installation for Holoeye SLM

In order to use the Holoeye LC 2012 SLM, you will need to manually download Holoeye's [SLM Display
SDK](https://customers.holoeye.com/slm-display-sdk-v3-0-for-python-windows/) and
install it. Unfortunately, `only Windows operating systems are currently supported by the SDK!` Just
follow the installation instructions. At runtime of this project's code, the script `slm_controller/holoeye` automatically determines the specific path of your SDK installation. But note that this step is
not a requirement for the other SLMs to work.

## Example scripts

In `examples` you can find various example scripts that show how to control the
supported SLMs.

First, activate the virtual environment:

```sh
source .slm_controller_env/bin/activate
```

You can exit the virtual environment by running `deactivate`.

### Adafruit SLM

This script controls the SLM isolated from the [Adafruit 1.8" TFT
LCD](https://learn.adafruit.com/1-8-tft-display/overview). It either allows
to show an image specified by its path or a random pattern. By default RGB is
used but you can also use monochrome images instead. Another flag allows to
define how the aspect ratio is handled.

```sh
$ python examples/adafruit_slm.py --help
Usage: adafruit_slm.py [OPTIONS]

Options:
  --file_path TEXT      Path to image to display, create random pattern if
                        None.
  --monochrome          Show monochrome image, otherwise use RGB.
  --not_original_ratio  Reshape which can distort the image, otherwise scale
                        and crop to match original aspect ratio.
  --help                Show this message and exit.
```

To display a randomly generated grayscale image:

```sh
python examples/adafruit_slm.py --monochrome
```

For a randomly generated RGB image:

```sh
python examples/adafruit_slm.py
```

For an image, you can pass the file path:

```sh
python examples/adafruit_slm.py --filepath images/blinka.jpg
```

The original image will be rescaled and cropped to match the original aspect ratio.

### Nokia SLM

This script controls the [Nokia 5110
LCD](https://learn.adafruit.com/nokia-5110-3310-monochrome-lcd) SLM. Like
before, it either allows
to show an image specified by its path or a random pattern. Note that this SLM
only supports monochrome values. A flag allows to
define how the aspect ratio is handled.

```sh
$ python examples/nokia_slm.py --help
Usage: nokia_slm.py [OPTIONS]

Options:
  --file_path TEXT      Path to image to display, create random pattern if
                        None.
  --not_original_ratio  Reshape which can distort the image, otherwise scale
                        and crop to match original aspect ratio.
  --help                Show this message and exit.
```

### Holoeye SLM

This script controls the [Holoeye LC
2012](https://holoeye.com/lc-2012-spatial-light-modulator/) SLM. Here too, it either
allows to show an image specified by its path or a random pattern. Note that only
monochrome values are supported by this SLM. A flag allows to
define how the aspect ratio is handled. Another float argument permits to set
how long the pattern is shown for.

<!-- TODO needed for CITL, add to other SLMs too? -->

```sh
$ python examples/holoeye_slm.py --help
Usage: holoeye_slm.py [OPTIONS]

Options:
  --file_path TEXT      Path to image to display, create random pattern if
                        None.
  --not_original_ratio  Reshape which can distort the image, otherwise scale
                        and crop to match original aspect ratio.
  --show_time FLOAT     Time to show the pattern on the SLM, show indefinitely
                        if None.
  --help                Show this message and exit.
```

## Adding a new SLM

In order to add support for a new SLM, a few steps need to be taken. These are
done to avoid hard-coded values, but rather have global variables/definitions
that are accessible throughout the whole code base.

1. Add SLM configuration in `slm_controller/hardware.py:slm_devices`.
2. Define a new class in `slm_controller/slm.py` for interfacing with the new SLM component (set parameters, patterns, etc).
3. Add to factory method `create` in `slm_controller/slm.py` for a conveniently one-liner to instantiate an object of the new SLM component.
