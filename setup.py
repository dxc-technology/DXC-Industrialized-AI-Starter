from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


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
    install_requires=["JIRA>=3.0.1","scikit-learn>=0.24.2","Algorithmia>=1.10.0","gitpython>=3.1.18","flatten_json==0.1.13","pyjanitor>=0.21.0","ftfy>=6.0.3","arrow>=1.1.1","pandas-profiling[notebook]==2.9.0",
                      "scrubadub>=1.2.2","yellowbrick==1.1","datacleaner>=0.1.5","missingno>=0.5.0","pymongo>=3.12.0","IPython>=7.26.0","dnspython>=2.1.0","pmdarima>=1.8.2","pyaf>=3.0","interpret-community>=0.19.2","flask_cors>=3.0.10","gevent>=21.8.0","tpot>=0.11.7","feature_engine>=1.1.1","tensorflow>=2.6.0","ktrain>=0.27.2","raiwidgets>=0.9.3","pandas>=1.3.2","janitor", "gym==0.18.0","keras-rl2>=1.0.5"],
    entry_points={
        "console_scripts": [
            "dxc=dxc.ai:main",
        ]
    },
#     package_data={'datasets/data': ['datasets/data/*'],},
    include_package_data=True,
)
