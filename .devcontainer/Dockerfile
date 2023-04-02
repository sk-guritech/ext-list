FROM alpine:3.17.3

ENV ENV "/root/.ashrc"
ENV PYTHON_VERSIONS="3.7.16 3.8.16 3.9.16 3.10.10 3.11.2 3.12.0a6"

COPY ./python-settings/requirements.txt /root/requirements.txt

RUN apk update && \
    apk add --no-cache git bash build-base libffi-dev openssl-dev bzip2-dev zlib-dev readline-dev sqlite-dev g++ musl-dev linux-headers libc-dev && \
    \
    git clone https://github.com/pyenv/pyenv.git ~/.pyenv && \
    for PYTHON_VERSION in $PYTHON_VERSIONS; do \
        ~/.pyenv/bin/pyenv install ${PYTHON_VERSION}; \
        /root/.pyenv/versions/${PYTHON_VERSION}/bin/pip install --upgrade pip; \
        /root/.pyenv/versions/${PYTHON_VERSION}/bin/pip install -r /root/requirements.txt; \
    done \
    && echo "alias python='/root/.pyenv/versions/3.7.16/bin/python'" >> ~/.ashrc \
    && echo "alias python3='/root/.pyenv/versions/3.7.16/bin/python'" >> ~/.ashrc \
    && echo "alias pip='/root/.pyenv/versions/3.7.16/bin/pip'" >> ~/.ashrc \
    && echo "alias pip3='/root/.pyenv/versions/3.7.16/bin/pip'" >> ~/.ashrc

ENV PATH /root/.pyenv/versions/3.7.16/bin:${PATH}
ENV PATH /root/.pyenv/versions/3.8.16/bin:${PATH}
ENV PATH /root/.pyenv/versions/3.9.16/bin:${PATH}
ENV PATH /root/.pyenv/versions/3.10.10/bin:${PATH}
ENV PATH /root/.pyenv/versions/3.11.2/bin:${PATH}
ENV PATH /root/.pyenv/versions/3.12.0a6/bin:${PATH}
