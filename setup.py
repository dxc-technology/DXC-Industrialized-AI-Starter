from setuptools import setup, find_packages
import pathlib
import pkg_resources
import subprocess
import os

def readme():
    with open('README.md') as f:
        README = f.read()
    return README

#Getting the version number from Git
version_number = (
    subprocess.run(["git", "describe", "--tags"], stdout=subprocess.PIPE)
    .stdout.decode("utf-8")
    .strip()
)
assert "." in version_number

assert os.path.isfile("version.py")
with open("VERSION", "w", encoding="utf-8") as fh:
    fh.write(f"{version_number}\n")

with pathlib.Path('requirements.txt').open() as requirements_txt:
    install_requires = [
        str(requirement)
        for requirement
        in pkg_resources.parse_requirements(requirements_txt)
    ]

setup(
    name="DXC-Industrialized-AI-Starter",
    version= version_number, 
    description="Python library which is extensively used for all AI projects",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/dxc-technology/DXC-Industrialized-AI-Starter",
    #download_url = "https://github.com/dxc-technology/DXC-Industrialized-AI-Starter/releases/tag/v1.0.tar.gz",
    author="DXC",
    license="Apache License 2.0",
    platforms='any',
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.7",
    ],
    #packages=["dxc", "dxc.ai"],
    packages=find_packages(),
#     include_package_data=True,
    install_requires= install_requires,
    entry_points={
        "console_scripts": [
            "dxc=dxc.ai:main",
        ]
    },
#     package_data={'datasets/data': ['datasets/data/*'],},
    package_data={"DXC-Industrialized-AI-Starter": ["VERSION"]},
    include_package_data=True,
)
