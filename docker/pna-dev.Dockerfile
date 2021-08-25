FROM python:3.9

RUN apt-get update -y
RUN apt-get install -y fonts-noto-cjk cron

RUN pip install --upgrade pip
COPY requirements.txt /temp/requirements.txt
RUN pip install -r /temp/requirements.txt
RUN rm -r /temp
