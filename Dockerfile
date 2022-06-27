FROM ubuntu:20.04

ENV PYTHONIOENCODING=utf-8
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y python3-pip

WORKDIR /home/ubuntu/travel_calculator

RUN pip3 install pip --upgrade && \
    pip3 install poetry
COPY requirements.txt ./
RUN pip3 install -r requirements.txt
RUN pip list
COPY . .


EXPOSE 8000
#CMD python3 manage.py runserver 0.0.0.0:8000
CMD uwsgi -i uwsgi.ini
