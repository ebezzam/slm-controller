import matplotlib.pyplot as plt
from slm_controller.simulate_prop import lens_prop, lensless_prop
from slm_controller.transform_fields import (
    load_holoeye,
    holoeye_to_lensless_setting,
)


def simulate_prop_holoeye():
    holoeye_slm_field = load_holoeye()

    slm_field = holoeye_slm_field[0, 0, :, :]
    propped_slm_field = lens_prop(holoeye_slm_field)[0, 0, :, :]
    show_plot(slm_field, propped_slm_field, "Holoeye with lens")

    holoeye_slm_field = holoeye_to_lensless_setting(holoeye_slm_field)
    slm_field = holoeye_slm_field[0, 0, :, :]
    propped_slm_field = lensless_prop(holoeye_slm_field)[0, 0, :, :]
    show_plot(slm_field, propped_slm_field, "Holoeye without lens")


def show_plot(slm_field, propped_slm_field, title):
    # plot
    fig = plt.figure()
    fig.suptitle(title)
    ax1 = fig.add_subplot(221)
    ax2 = fig.add_subplot(222)
    ax3 = fig.add_subplot(223)
    ax4 = fig.add_subplot(224)
    ax1.title.set_text("Phase on SLM")
    ax2.title.set_text("Amplitude on SLM")
    ax3.title.set_text("Phase after propagation to screen")
    ax4.title.set_text("Amplitude after propagation to screen")
    ax1.imshow(slm_field.angle())
    ax2.imshow(slm_field.abs())
    ax3.imshow(propped_slm_field.angle())
    ax4.imshow(propped_slm_field.abs())
    plt.show()


if __name__ == "__main__":
    simulate_prop_holoeye()
