FROM ubuntu:20.04 as builder

RUN mkdir /data
        
WORKDIR /data

RUN git clone https://github.com/yeastgenome/SGDBackend_docker.git

FROM ubuntu:20.04

RUN DEBIAN_FRONTEND=noninteractive apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get upgrade -y \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y \
        apache2 \
        make \
	postfix \
        python3-pip \
    && pip3 install virtualenv 

WORKDIR /data
RUN mkdir www \
    && cd www \
    && mkdir logs

WORKDIR /data/www
COPY --from=builder /data/SGDBackend_docker/www .

RUN virtualenv venv && . venv/bin/activate

WORKDIR /data/www/SGDBackend
COPY prod_variables.sh .
RUN make build \ 
    && python scripts/disambiguation/index_disambiguation.py \
    && . prod_variables.sh \
    && pserve development.ini --reload > /data/www/logs/error.log 2>&1 &

WORKDIR /

CMD ["apachectl", "-D", "FOREGROUND"]
