# pull official base image
FROM python:3.7.9-slim-stretch as builder
ARG OPENBABEL_TAG="openbabel-2-4-1"

RUN apt-get update \
    && apt-get install -y \
        libc6-dev \
        gcc \
        wget \
        mime-support \
        libpcre3 libpcre3-dev \
        vim \
        swig \
        git \
        cmake \
        g++ \
        libxml2 \
        swig \
        parallel \
    && apt-get clean

# Install OpenJDK-8
RUN mkdir -p /usr/share/man/man1
RUN apt-get update && \
    apt-get install -y openjdk-8-jdk && \
    apt-get install -y ant && \
    apt-get clean;

# Fix certificate issues
RUN apt-get update && \
    apt-get install ca-certificates-java && \
    apt-get clean && \
    update-ca-certificates -f;

# Setup JAVA_HOME -- useful for docker commandline
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64/
RUN export JAVA_HOME

## Install miniconda
RUN wget -q -P /tmp \
  https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && bash /tmp/Miniconda3-latest-Linux-x86_64.sh -b -p /opt/conda \
    && rm /tmp/Miniconda3-latest-Linux-x86_64.sh

# Install conda packages.
ENV PATH="/opt/conda/bin:$PATH"

# Copy env requirement file
COPY ./dyscore2.yml /app/dyscore/dyscore2.yml
COPY ./dyscore3.yml /app/dyscore/dyscore3.yml
COPY ./requirements.txt /app/dyscore/requirements.txt

# Create virtual env for py27
RUN conda env create --name dyscore2 -f /app/dyscore/dyscore2.yml python=2.7


# Create virtual env for py37
RUN conda env create --name dyscore3 -f /app/dyscore/dyscore3.yml python=3.7
# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "dyscore3", "/bin/bash", "-c"]
RUN /opt/conda/envs/dyscore3/bin/pip --no-cache-dir install -r /app/dyscore/requirements.txt

# Copy other files
COPY ./ /app/dyscore

# set work directory
WORKDIR /app/dyscore

## Create the user that will run the app
RUN adduser --disabled-password --gecos '' dyscore-user
RUN chown -R dyscore-user:dyscore-user ./
USER dyscore-user

## Not necessary, since we add conda virtual env to the ENTRYPOINT
RUN echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate dyscore3" >> ~/.bashrc

RUN yes 'will cite' | parallel --citation

#  Prevents Python from writing pyc files to disc (equivalent to python -B option
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout and stderr (equivalent to python -u option)
ENV PYTHONUNBUFFERED 1

RUN chmod +x /app/dyscore/run_dyscore
ENTRYPOINT ["/app/dyscore/run_dyscore"]


