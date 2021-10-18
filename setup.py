from setuptools import setup, find_packages
import pathlib
import pkg_resources
import setuptools

def readme():
    with open('README.md') as f:
        README = f.read()
    return README

with pathlib.Path('requirements.txt').open() as requirements_txt:
    install_requires = [
        str(requirement)
        for requirement
        in pkg_resources.parse_requirements(requirements_txt)
    ]

setup(
    name="DXC-Industrialized-AI-Starter",
    version="3.1.1",
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
    include_package_data=True,
)
