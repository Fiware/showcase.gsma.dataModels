FROM python:3.7.2-alpine3.8

COPY harvester.py /opt/
COPY config.example.yml /opt/

RUN pip3 install pytz==2018.9 pyaml==3.13 aiohttp==3.5.4 requests==2.19.1 \
&&  chmod +x /opt/*.py

WORKDIR /opt/

ENTRYPOINT ["python3", "-u", "/opt/harvester.py"]
