# SLM controller

Scripts and modules to control displays with Python.

Note that our convention for dimension order is (channels, height, width).

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


#### No Raspberry Pi?

You can still try out some features of this library by running:
```sh
pip install -e .[dev]
```

You won't be able to run any examples that use the display.

## Example scripts

In `examples` are various example scripts to control an RGB and a monochrome (binary) display by 
Adafruit.

First, activate the virtual environment:

```sh
source photonics_env/bin/activate
```
You can exit the virtual environment by running `deactivate`.


#### RGB display

To display a randomly generated grayscale image:

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


#### Monochrome display

To display a randomly generated monochrome image:

```sh
python examples/binary_display.py
```

For an image, you can pass the file path:

```sh
python examples/binary_display.py --file_path examples/blinka.jpg
```

The original image will be rescaled and cropped to match the original aspect ratio.

With the following command, a simple reshape will be performed which can distort the original image.

```sh
python examples/binary_display.py --file_path examples/blinka.jpg --not_original_ratio
```


#### Aperture

To set a defined aperture shape, check out the following script:
```
>> python examples/set_aperture.py --help

Usage: set_aperture.py [OPTIONS]

  Set aperture on a physical device.

Options:
  --shape [rect|square|line|circ]
                                  Shape of aperture.
  --n_cells INTEGER               Side length for 'square', length for 'line',
                                  radius for 'circ'. To set shape for 'rect',
                                  use`rect_shape`.

  --rect_shape INTEGER...         Shape for 'rect' in number of cells; `shape`
                                  must be set to 'rect'.

  --vertical                      Whether line should be vertical (True) or
                                  horizontal (False).

  --device [rgb|binary]           Which device to program with aperture.
  --help                          Show this message and exit.
```

For example, to create a circle aperture on the monochrome device with a radius of 20 cells:
```sh
python examples/set_aperture.py --device binary --shape circ --n_cells 20
```

For a square aperture on the RGB device with a side length of 2 cells:
```sh
python examples/set_aperture.py --device rgb --shape square --n_cells 2
```

You can preview an aperture with the following script. Note that it should be run on a machine with
plotting capabilities, i.e. with `matplotlib`.
```
>> python examples/plot_aperture.py --help

Usage: plot_aperture.py [OPTIONS]

  Plot SLM aperture.

Options:
  --shape [rect|square|line|circ]
                                  Shape of aperture.
  --n_cells INTEGER               Side length for 'square', length for 'line',
                                  radius for 'circ'. To set shape for 'rect',
                                  use`rect_shape`.

  --rect_shape INTEGER...         Shape for 'rect' in number of cells; `shape`
                                  must be set to 'rect'.

  --vertical                      Whether line should be vertical (True) or
                                  horizontal (False).

  --show_tick_labels              Whether or not to show cell values along
                                  axes.

  --cell_dim FLOAT...             Shape of cell in meters (height, width).
  --slm_shape INTEGER...          Dimension of SLM in number of cells (height,
                                  width).

  --monochrome                    Whether SLM is monochrome.
  --device [rgb|binary]           Which device to program with aperture.
  --help                          Show this message and exit.
```