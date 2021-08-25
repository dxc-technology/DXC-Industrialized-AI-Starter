from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        README = f.read()
    return README
def read_requirements():
    with open('requirements.txt') as f:
        required = f.read().splitlines()
    return required

setup(
    name="DXC-Industrialized-AI-Starter",
    version="2.3.9",
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
    install_requires= ["JIRA","scikit-learn==0.22.2.post1","auto_ml","Algorithmia==1.7.8","gitpython","flatten_json==0.1.13","pyjanitor","ftfy","arrow","pandas-profiling[notebook]==2.9.0",
                      "scrubadub","yellowbrick==1.1","datacleaner","missingno","pymongo","IPython","dnspython","pmdarima","pyaf","interpret-community","flask_cors","gevent","tpot","feature_engine","tensorflow","ktrain","raiwidgets","pandas","janitor", "gym==0.18.0","keras-rl2","tensorflow"],
    entry_points={
        "console_scripts": [
            "dxc=dxc.ai:main",
        ]
    },
#     package_data={'datasets/data': ['datasets/data/*'],},
    include_package_data=True,
)
