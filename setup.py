import setuptools

setuptools.setup(
    name="PImatrix",
    version="0.0.1",
    author="Ferdinand Thiessen",
    author_email="rpm@fthiessen.de",
    description="Controller for the stage LED matrix @ClubAquariumDD",
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=["pyaudio", "numpy", "rpi_ws281x"],
    scripts=['bin/pimatrix']
)
