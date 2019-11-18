FROM ubuntu:19.04
MAINTAINER Abhishek N. Kulkarni <ankulkarni@wpi.edu>


RUN echo 'Etc/UTC' > /etc/timezone && \
    ln -s /usr/share/zoneinfo/Etc/UTC /etc/localtime && \
    apt-get update && apt-get install -q -y tzdata && rm -rf /var/lib/apt/lists/*


RUN apt update && \
	RUNLEVEL=1 DEBIAN_FRONTEND=noninteractive && \
	apt-get install -y software-properties-common wget nano make gcc g++ gnupg2 git

# Install python packages
RUN apt-get install -y python3-dev python3-pip python3-sphinx
RUN pip3 install pytest numpy sphinx_rtd_theme recommonmark

# Configure spot repositories for download.
RUN wget -q -O - https://www.lrde.epita.fr/repo/debian.gpg | apt-key add - && \
	echo 'deb http://www.lrde.epita.fr/repo/debian/ stable/' >> /etc/apt/sources.list

# Install spot
RUN apt-get update && \
	RUNLEVEL=1 DEBIAN_FRONTEND=noninteractive && \
	apt-get install -y spot libspot-dev spot-doc python3-spot

# Install graph-tool
RUN echo 'deb http://downloads.skewed.de/apt/disco disco universe' >> /etc/apt/sources.list
RUN echo 'deb-src http://downloads.skewed.de/apt/disco disco universe' >> /etc/apt/sources.list
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 7A80C8ED4FCCBE09
RUN apt-get update && \
	RUNLEVEL=1 DEBIAN_FRONTEND=noninteractive && \
	apt-get install -y python3-graph-tool

# Get and install latest iglsynth
RUN pip3 install iglsynth --upgrade

# Install coverage tools
RUN pip3 install pytest-cov coverage codecov

# Install additional packages, libraries
RUN pip3 install matplotlib
