FROM ubuntu:19.10
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

# Install coverage tools
RUN pip3 install pytest-cov coverage codecov

# Install additional packages, libraries
RUN pip3 install matplotlib
RUN pip3 install snap-stanford
RUN pip3 install bidict

