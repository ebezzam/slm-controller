"""
Plotting utility function.
"""

import matplotlib.pyplot as plt


def show_plot(slm_field, propped_slm_field, title):
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
