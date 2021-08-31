from setuptools import setup, find_packages
import binio

__VERSION__ = "0.1.1"
__LICENSE__ = "GPLv3"
__AUTHOR__ = "Dobriakov Anton"
__AUTHOR_EMAIL__ = "anton.dobryakov@gmail.com"
__URL__ = "https://github.com/dobryak/pybinio"

setup(
    name="pybinio",
    version=__VERSION__,
    description="A convenient wrapper around the `struct` python module. "
                "It contains convenient reader and writer classes that can "
                "be used to write primitive data types in a specific byte order.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url=__URL__,
    author=__AUTHOR__,
    author_email=__AUTHOR_EMAIL__,
    packages=find_packages(exclude=["tests*"]),
    zip_safe=True,
    license=__LICENSE__,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    python_requires=">=3.9"
)
