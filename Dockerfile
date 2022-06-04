FROM ubuntu
WORKDIR /dl-schedule

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Kiev

RUN apt update
RUN apt install -y software-properties-common curl
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt update
RUN apt install -y python3.10 python3.10-distutils

# Install pip
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10

COPY app/ .

RUN python3.10 -m pip install -r requirements.txt

CMD [ "gunicorn", "--bind", "0.0.0.0:8005", "app:create_app()"]
