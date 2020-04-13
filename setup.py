from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="dxc",
    version="1.0",
    description="Python library which is extensively used for all AI projects",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/dxc-technology/DXC-Industrialized-AI-Starter.git",
    author="DXC",
    license="Apache License 2.0",
    classifiers=[
        "License :: OSI Approved :: Apache License 2.0 License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["dxc"],
    include_package_data=True,
    install_requires=["JIRA","auto_ml","Algorithmia","gitpython","flatten_json","pyjanitor","ftfy","arrow",
                      "scrubadub","yellowbrick","datacleaner","missingno","pymongo","IPython"],
    entry_points={
        "console_scripts": [
            "dxc=dxc.ai:main",
        ]
    },
)
