FROM python:3.6

RUN apt-get update && \
    apt-get install -y \
      apt-transport-https \
      ca-certificates \
      cmake \
      g++ && \
    echo "deb [trusted=yes] https://repo.quasardb.net/apt/ /" > /etc/apt/sources.list.d/quasardb.list && \
    apt-get update && \
    apt-get install -y qdb-api && \
    rm -rf /var/lib/apt/lists/*

RUN pip install prometheus_client==0.7.1 && \
    pip install wheel && \
    pip install quasardb==3.4.0 && \
    rm -rf /root/.cache
