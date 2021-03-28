FROM python:3.9.2-buster

RUN mkdir -p /home/courier_api
WORKDIR /home/courier_api
COPY . /home/courier_api

RUN apt update && \
    apt install --no-install-recommends -y gcc build-essential

ENV TZ=Europe/Moscow

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN pip install --no-cache-dir -r requirements.txt

CMD gunicorn --bind courier-api-1.0:5000 -w 2 wsgi:app
