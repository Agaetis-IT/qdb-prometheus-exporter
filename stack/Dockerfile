FROM python:3.6

RUN apt-get update

RUN pip install prometheus_client==0.7.1 && \
    pip install wheel && \
    pip install https://s3-eu-west-1.amazonaws.com/download.quasardb.net/quasardb/3.8/3.8.1/api/python/quasardb-3.8.1-cp36-cp36m-linux_x86_64.whl
