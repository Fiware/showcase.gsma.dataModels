FROM python:3.7.2-alpine3.8

COPY harvester.py /opt/
COPY config.example.yml /opt/

RUN pip3 install pytz pyaml aiohttp requests \
&&  chmod +x /opt/*.py

WORKDIR /opt/

ENTRYPOINT ["python3", "-u", "/opt/harvester.py"]
