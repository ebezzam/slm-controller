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
        "Operating System :: Generally OS independent but the Holoeye SLM is only supported on Windows",
    ],
    python_requires=">=3.6",  # TODO Newer python version?
    install_requires=[
        "adafruit-circuitpython-rgb-display",
        "adafruit-circuitpython-sharpmemorydisplay",
        "adafruit-circuitpython-pcd8544",
        "Pillow",
        "numpy",
        "matplotlib",
    ],
    extra_requires={  # TODO Does not seem to work on my machine, WARNING: slm-controller 0.0.2 does not provide the extra 'dev'
        "dev": ["click", "pytest", "black"],
    },
)
