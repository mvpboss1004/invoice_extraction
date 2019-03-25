FROM ubuntu:bionic

ENV LANG C.UTF-8  
ENV LC_ALL C.UTF-8 
ENV PYTHONIOENCODING utf-8   
ENV PYTHON_VERSION=3.6.6
ENV PYTHON_MAJOR=3.6

RUN \
    apt-get update -y \
    && apt-get install -y \
    curl \
    git \
    libzbar0 \
    mupdf \
    libzbar-dev \
    python3 \
    python3-dev \
    python3-pip \
    && pip3 install pip --upgrade 
    
COPY requirements.txt .
ADD . /code
WORKDIR /code

RUN pip3 install -r requirements.txt
