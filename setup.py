from setuptools import setup, find_packages
from iglsynth.version import get_publish_version, author



setup(
    name='iglsynth',
    packages=find_packages(),
    version=get_publish_version(),
    description='Infinite Games on graph and Logic-based controller Synthesis',
    author=author(),
    author_email='ankulkarni@wpi.edu',
    download_url=f'https://github.com/abhibp1993/iglsynth/releases/{get_publish_version()}.tar.gz',
    url='www.akulkarni.me/iglsynth',
    install_requires=['pytest'],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ])
