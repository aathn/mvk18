from distutils.command.install import install
from setuptools import setup, find_packages
import urllib.request
import os


class InstallWithMaestro(install):
    """Install and download maestro module"""

    def run(self):
        if not os.path.isfile("./skysensestreamer/maestro.py"):
            try:
                print("Attempting to download maestro")
                maestro_url = "https://raw.githubusercontent.com/FRC4564/maestro/master/maestro.py"
                urllib.request.urlretrieve(
                    maestro_url, filename="./skysensestreamer/maestro.py"
                )
                print("Successfully downloaded maestro")
            except:
                print(
                    'Failed to download maestro, manual download from "https://github.com/FRC4564/Maestro" required'
                )
        else:
            print("Maestro is already installed")

        install.run(self)


setup(
    name="skysensestreamer",
    description="Stream video of aircrafts",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.7",
    cmdclass={"install": InstallWithMaestro},
    install_requires=["pyserial==3.4", "numpy==1.16.1"],
)
