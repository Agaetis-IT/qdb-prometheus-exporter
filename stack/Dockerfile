FROM python:3.6

RUN apt update && \
    apt install apt-transport-https ca-certificates -y && \
    echo "deb [trusted=yes] https://repo.quasardb.net/apt/ /" > /etc/apt/sources.list.d/quasardb.list && \
    apt update && \
    apt install qdb-api=3.3.0-1 cmake g++ -y

RUN pip install prometheus_client && \
    pip install wheel && \
    pip install quasardb==3.3.2