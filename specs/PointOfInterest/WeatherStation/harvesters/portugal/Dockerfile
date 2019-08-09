FROM python:3.7.3-alpine3.10

LABEL maintainer="Dmitrii Demin <mail@demin.co>"

WORKDIR /opt/

COPY . /opt

RUN apk update && \
    apk add --no-cache git build-base curl && \
    pip install -r requirements.txt && \
    apk del build-base git && \
    rm -f /var/cache/apk/*

USER nobody

ENTRYPOINT ["/opt/entrypoint.sh"]
