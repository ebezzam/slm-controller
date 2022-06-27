import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="slm-controller",
    version="0.0.1",
    author="Eric Bezzam",
    author_email="ebezzam@gmail.com",
    description="Package to control spatial light modulators.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ebezzam/slm-controller",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Generally OS Independent but Holoeye SLM SDK is only available on Windows",
    ],
    python_requires=">=3.6",
    install_requires=[
        "adafruit-circuitpython-rgb-display",
        "adafruit-circuitpython-sharpmemorydisplay",
        "adafruit-circuitpython-pcd8544",
        "Pillow",
        "numpy",
        "matplotlib",
    ],
    extra_requires={"dev": ["click", "pytest"],},
)
