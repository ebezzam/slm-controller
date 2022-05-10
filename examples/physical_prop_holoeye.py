import click
from slm_controller import display
import slm_controller.neural_holography.utils as utils
from slm_controller.transform_fields import load_holoeye


@click.command()
@click.option("--show_time", type=float, default=5.0, help="Time to show the pattern on the SLM.")
def physical_prop_holoeye(show_time):
    holoeye_slm_field = load_holoeye().angle()
    holoeye_slm_field = utils.phasemap_8bit(holoeye_slm_field)

    D = display.HoloeyeDisplay(show_time)

    # display
    D.imshow(holoeye_slm_field)


if __name__ == "__main__":
    physical_prop_holoeye()
