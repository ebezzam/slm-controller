# slm-controller

Scripts and modules to control SLMs using Python.

Note that our convention for dimension order is (channels, height, width).

- [slm-controller](#slm-controller)
  - [Installation](#installation)
    - [Adafruit and Nokia SLMs installation](#adafruit-and-nokia-slms-installation)
    - [No Raspberry Pi?](#no-raspberry-pi)
    - [Holoeye SLM installation](#holoeye-slm-installation)
    - [Manual installation for Holoeye SLM](#manual-installation-for-holoeye-slm)
  - [Example scripts](#example-scripts)
    - [Adafruit RGB SLM](#adafruit-rgb-slm)
    - [Adafruit Monochrome SLM](#adafruit-monochrome-slm)
    - [Nokia SLM](#nokia-slm)
    - [Holoeye SLM](#holoeye-slm)
  - [Adding a new SLM](#adding-a-new-slm)

The main goal of the project is to provided an abstraction level for different
SLM devices allowing to use them interchangeably for different applications.

Generally speaking there are two different kinds of SLMs: amplitude and phase
SLM. Both kinds simply modulate different properties of light. Currently the
project supports 4 different SLMs device.

Amplitude SLMs:

- [Adafruit 1.8" TFT LCD](https://learn.adafruit.com/1-8-tft-display/overview) (RGB)
- [Adafruit 1.3" Sharp Memory
  LCD](https://learn.adafruit.com/adafruit-sharp-memory-display-breakout)
  (Binary monochrome)
- [Nokia 5110 LCD](https://learn.adafruit.com/nokia-5110-3310-monochrome-lcd) (Monochrome)

<!-- TODO Holoeye actually can do both via polarization modulation and combination with polarizer/analyzer -->

Phase SLMs:

- [Holoeye LC 2012](https://holoeye.com/lc-2012-spatial-light-modulator/)

Note that if anything goes wrong
with the communication with those devices the phase maps are simply plotted
instead of being shown on the devices themselves.

## Installation

### Adafruit and Nokia SLMs installation

The target platform is a Raspberry Pi. After cloning this repository, you can
install the necessary dependencies by running the following script:

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
pip install -e .[dev] #TODO does not work, dev not found
```

### No Raspberry Pi?

You can still try out some features of this library! You won't be able to run
any examples programs on the physical SLMs but the results will be plotted to
your screen instead as mentioned earlier.

### Holoeye SLM installation

The SDK needed for [Holoeye LC
2012](https://holoeye.com/lc-2012-spatial-light-modulator/) `is only supported on Windows operating systems!` Hence a Raspberry Pi directly is impossible. A
device
with a live Windows instance is needed to use the Holoeye SLM. In the future we will
check if Windows running inside a container on a Raspberry Pi is an option
though.

<!-- TODO check windows in a container -->

Additionally, you need to perform some manual installation, explained in the
next section, after having run the script mentioned above.

### Manual installation for Holoeye SLM

For being able to use using the Holoeye LC
2012 SLM implemented in the
project you will need to manually download Holoeye's [SLM Display
SDK](https://customers.holoeye.com/slm-display-sdk-v3-0-for-python-windows/) and
install it. Unfortunately, `only Windows operating systems are supported currently by the SDK!` Just
follow the installation instructions. The script located at
`slm_controller/holoeye` is then determining the specific path to your installation of the
SDK automatically at runtime whenever it is needed.

## Example scripts

In `examples` you can find various example scripts that control an RGB and a binary
(monochrome) Adafruit SLM, a Nokia SLM and a Holoeye SLM.

First, activate the virtual environment:

```sh
source .slm_controller_env/bin/activate
```

You can exit the virtual environment by running `deactivate`.

<!-- TODO is it okay to call them SLMs instead of displays? -->

### Adafruit RGB SLM

This script controls the [Adafruit 1.8" TFT
LCD](https://learn.adafruit.com/1-8-tft-display/overview) SLM. It either allows
to show an image specified by its path or a random pattern. By default RGB is
used but you can also use grayscale images instead. Another flag allows to
define how the aspect ratio is handled.

```sh
$ python examples/rgb_slm.py --help
Usage: rgb_slm.py [OPTIONS]

Options:
  --file_path TEXT      Path to image to display, create random pattern if
                        None.
  --monochrome           Show monochrome image, otherwise use RGB.
  --not_original_ratio  Reshape which can distort the image, otherwise scale
                        and crop to match original aspect ratio.
  --help                Show this message and exit.
```

To display a randomly generated grayscale image:

```sh
python examples/rgb_display.py --monochrome
```

For a randomly generated RGB image:

```sh
python examples/rgb_display.py
```

For an image, you can pass the file path:

```sh
python examples/rgb_display.py --filepath images/blinka.jpg
```

The original image will be rescaled and cropped to match the original aspect ratio.

### Adafruit Monochrome SLM

This script controls the [Adafruit 1.3" Sharp Memory LCD](https://learn.adafruit.com/adafruit-sharp-memory-display-breakout) SLM. It either allows
to show an image specified by its path or a random pattern. Note that only
binary monochrome values are supported by this SLM. A flag allows to
define how the aspect ratio is handled.

```sh
$ python examples/binary_slm.py --help
Usage: binary_slm.py [OPTIONS]

Options:
  --file_path TEXT      Path to image to display, create random pattern if
                        None.
  --not_original_ratio  Reshape which can distort the image, otherwise scale
                        and crop to match original aspect ratio.
  --help                Show this message and exit.
```

To display a randomly generated monochrome image:

```sh
python examples/binary_display.py
```

For an image, you can pass the file path:

```sh
python examples/binary_display.py --file_path images/blinka.jpg
```

The original image will be rescaled and cropped to match the original aspect ratio.

With the following command, a simple reshape will be performed which can distort the original image.

```sh
python examples/binary_display.py --file_path images/blinka.jpg --not_original_ratio
```

### Nokia SLM

This script controls the [Nokia 5110 LCD](https://learn.adafruit.com/nokia-5110-3310-monochrome-lcd) SLM. It either allows
to show an image specified by its path or a random pattern. Note that only
monochrome values are supported by this SLM. A flag allows to
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

This script controls the [Holoeye LC 2012](https://holoeye.com/lc-2012-spatial-light-modulator/) SLM. It either allows
to show an image specified by its path or a random pattern. Note that only
monochrome values are supported by this SLM. A flag allows to
define how the aspect ratio is handled. A float argument permits to set the time
how long the pattern is shown.

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

1. Add configuration in `slm_controller/hardware.py:slm_devices`.
2. Create class in `slm_controller/slm.py`.
3. Add to factory method `create_slm` in `slm_controller/slm.py`.
