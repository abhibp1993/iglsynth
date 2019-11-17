from setuptools import setup, find_packages



setup(
    name='iglsynth',
    packages=find_packages(),
    version='0.2.1',
    description='Infinite Games on graph and Logic-based controller Synthesis',
    author='Abhishek N. Kulkarni',
    author_email='ankulkarni@wpi.edu',
    download_url='https://github.com/abhibp1993/iglsynth/releases/0.2.1.tar.gz',
    url='iglsynth.akulkarni.me/en/latest/',
    install_requires=['pytest'],
    classifiers=[
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
