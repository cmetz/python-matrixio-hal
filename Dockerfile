FROM resin/raspberrypi3-debian:stretch
WORKDIR /usr/src/matrixio_hal
RUN apt-get update && \
    apt-get dist-upgrade && \
    apt-get install apt-transport-https build-essential python python-pip python-setuptools python-dev cython curl && \
    curl https://apt.matrix.one/doc/apt-key.gpg | apt-key add - && \
    echo "deb https://apt.matrix.one/raspbian stretch main" > /etc/apt/sources.list.d/matrixlabs.list && \
    apt-get update && \
    apt-get install libmatrixio-creator-hal-dev && \
    rm -rf /var/lib/apt/lists/*
COPY matrixio_hal/ ./matrixio_hal/
COPY setup.py .
RUN python setup.py install
WORKDIR /usr/src/app
COPY examples/*.py ./
ENTRYPOINT ["/sbin/tini", "-g",  "--"]
STOPSIGNAL SIGTERM
CMD [ "python", "./led_rotate.py" ]
