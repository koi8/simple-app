FROM python:alpine3.7
COPY app/* /app/
WORKDIR /app
RUN set -e; \
    apk add --no-cache --virtual build-deps \
        gcc \
        libc-dev \
        linux-headers \
    && pip install -r requirements.txt \
    && apk del build-deps
EXPOSE 5000
ENV prometheus_multiproc_dir=multiproc-tmp
CMD rm -rf multiproc-tmp && mkdir multiproc-tmp && python ./index.py

