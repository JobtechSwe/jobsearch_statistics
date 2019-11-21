FROM python:slim

EXPOSE 8000

RUN apt-get update && apt-get upgrade -y && \
    apt-get -y install \
        #python3 \
        #python3-pip \
        python3-dev \
        build-essential \
        nginx \
        git \
        curl && \
        apt-get clean

ENV TZ=Europe/Stockholm

COPY . /app

RUN date +"%Y-%m-%dT%H:%M:%S %Z" && \
    mkdir -p /var/run/nginx && \
    chmod -R 777 /var/run/nginx && \
    chmod -R 775 /app && \
    chmod -R 777 /usr/sbin && \
    #chmod -R 775 /usr/lib/python* && \
    chmod -R 777 /var/lib/nginx && \
    chmod -R 777 /var/log/* && \
    mkdir -p /var/tmp && \
    chmod -R 777 /var/tmp/

WORKDIR /app

RUN python3 -m pip install --upgrade setuptools
RUN python3 -m pip install gunicorn
RUN python3 -m pip install -r requirements.txt

USER 10000
CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:8000", "-k", "uvicorn.workers.UvicornWorker", "searchstatistics.main:app"]