Installation Instructions
=========================

IGLSynth requires Python (>= 3.7) and spot (>=2.7).
The recommended operating system is Ubuntu 19.04 or above, which ships with Python 3.7.
This allows spot and iglsynth to be installed directly using apt-get and pip, respectively.

If you want to use a different operating system, docker is the way to go! Please refer to the
docker installation instructions below.



Ubuntu 19.04 or above
---------------------

First, install spot using instructions given at `install spot <https://spot.lrde.epita.fr/install.html>`_.

Then, install IGLSynth::

    $ pip3 install iglsynth


Docker Image (other OS)
-----------------------

When using some other OS where either spot or iglsynth is not installed,
it is recommended to use `Docker <https://www.docker.com/>`_
images with an Python IDE such as `PyCharm <https://www.jetbrains.com/pycharm/>`_.
Note that using PyCharm is not necessary, but definitely makes life easy!!


Assuming Docker client is already installed on your OS, IGLSynth docker image can be
downloaded by running::

    $ docker pull abhibp1993/iglsynth

The instructions to set up remote interpreter are given at
`Configure a Remote Interpreter using Docker
<https://www.jetbrains.com/help/pycharm/using-docker-as-a-remote-interpreter.html>`_.


The above image also has ``numpy, matplotlib`` pre-installed.


Docker Image for Developers
---------------------------

**This section is only for developers of IGLSynth.**


IGLSynth development requires additional tools such as  pytest (testing), pytest-cov
(coverage checking), sphinx (automatic documentation), sphinx_rtd_theme (theme for sphinx documentation).
These all tools are installed in the developer image of docker (tagged ``dev``), in addition to spot.


**Note:** IGLSynth is **NOT** installed in developer's docker image. Developers are expected to mount
the necessary folders for development.


You can download the developer image of IGLSynth by running::

    $ docker pull abhibp1993/iglsynth:dev

and configure the remote interpreter with PyCharm using instructions given at
`Configure a Remote Interpreter using Docker
<https://www.jetbrains.com/help/pycharm/using-docker-as-a-remote-interpreter.html>`_.
