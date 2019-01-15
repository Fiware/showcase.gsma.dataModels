FROM alpine:3.8

COPY harvester.py /opt/
COPY config.yml /opt/

RUN apk add --no-cache --update python3 py3-requests py3-yaml \
&&  chmod +x /opt/*.py

WORKDIR /opt/

ENTRYPOINT ["python3", "-u", "/opt/harvester.py"]
