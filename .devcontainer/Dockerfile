FROM python:3.10.10-alpine
WORKDIR /tmp
COPY ./python-settings/requirements.txt /tmp/

RUN pip install -r /tmp/requirements.txt
RUN apk add git
RUN apk add bash
RUN apk add gcc g++ make gfortran
