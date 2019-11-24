"""Setup tools packaging information."""

from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

requires = [
    "requests",
    "pytest",
    "coverage",
]

open(os.path.join(here, "requirements.txt"), "w").writelines(
    [line + "\n" for line in requires]
)

setup(
    name="swagkar",
    version="20191124",
    description="Swagger Parser & Runner Utility",
    long_description="This utility is intended to ease the use of 3rd-party APIs which is based on Swagger",
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP",
    ],
    author="Alireza Hoseini",
    author_email="alireza.stack@gmail.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
)