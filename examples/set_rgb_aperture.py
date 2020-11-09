from slm_controller import display, aperture


# instantiate display object
D = display.RGBDisplay()
print(f"SLM dimension : {D.shape}")

# create aperture mask
apert_dim = (20, 20)
print(f"Aperture dimension : {apert_dim}")
ap = aperture.RectAperture(apert_dim=apert_dim, slm_dim=D.shape)

# set aperture
D.imshow(ap.mask)
