FROM alpine:3.8

COPY harvester.py /opt/
COPY stations.csv /opt/

RUN apk add --no-cache --update python3 py3-tz py3-requests \
&&  chmod +x /opt/*.py

WORKDIR /opt/

ENTRYPOINT ["python3", "-u", "/opt/harvester.py"]
