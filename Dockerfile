FROM python:3.7-slim-buster

RUN apt-get update 
RUN DEBIAN_FRONTEND=noninteractive \
    apt-get install -y wget build-essential

RUN python3 -m venv /venv

COPY requirements.txt /requirements.txt
RUN /venv/bin/pip install --disable-pip-version-check -r ./requirements.txt

ENV PATH="/venv/bin:$PATH"
