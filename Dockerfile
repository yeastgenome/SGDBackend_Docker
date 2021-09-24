FROM ubuntu:20.04

RUN DEBIAN_FRONTEND=noninteractive apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get upgrade -y \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y \
        apache2 \
        redis-server \
	make \
        python3-pip \
    && pip3 install virtualenv 

RUN mkdir /data
    && cd /data \
    && mkdir www \
    && cd /data/www \
    && mkdir logs

WORKDIR /data/www
COPY www .
RUN virtualenv venv && . venv/bin/activate

WORKDIR /data/www/SGDBackend
RUN make build \ 
    && python scripts/disambiguation/index_disambiguation.py \
    && . prod_variables.sh \
    && pserve development.ini --reload > /data/www/logs/error.log 2>&1 &

WORKDIR /

CMD ["apachectl", "-D", "FOREGROUND"]
