FROM ubuntu:latest

WORKDIR /usr/src/app

# Install Python 3.10
RUN apt-get update && \
    apt -f install && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y python3.10 python3.10-distutils && \
    apt-get clean

# Install pip
RUN apt-get update && apt-get install -y python3-pip

# Install graphviz
RUN apt-get update && apt-get install -y graphviz

# Make python3.11 the default python
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.10 1

# Set python3.11 as the default python3
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1

COPY . .

RUN pip3 install -r requirements.txt
