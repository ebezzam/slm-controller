import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="slm-controller",
    version="0.0.2",
    author="Eric Bezzam",
    author_email="ebezzam@gmail.com",
    description="Package to control spatial light modulators (SLMs).",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ebezzam/slm-controller",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS independent for previewing. See README for which OS is supported for which device",
    ],
    python_requires=">=3.8",
    install_requires=[
        "adafruit-circuitpython-rgb-display",
        "adafruit-circuitpython-sharpmemorydisplay",
        "adafruit-circuitpython-pcd8544",
        "Pillow",
        "numpy",
        "matplotlib",
    ],
    extra_requires={"dev": ["click", "black"],},
)
