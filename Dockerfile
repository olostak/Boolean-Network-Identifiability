FROM ubuntu:latest

RUN apt update -y && apt upgrade -y && \
     apt-get install -y --no-install-recommends apt-utils && \
    apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget libbz2-dev -y && \
    cd /usr/src && \
    wget https://www.python.org/ftp/python/3.11.4/Python-3.11.4.tgz && \
    tar xzf Python-3.11.4.tgz && \
    cd Python-3.11.4 && \
    ./configure --enable-optimizations && \
    make && \
    make altinstall && \
    python3.11 --version

RUN apt-get update && apt-get install -y python3.11 python3-distutils python3-pip python3-apt

WORKDIR /usr/app/src

COPY . .

RUN pip install -r requirements.txt
