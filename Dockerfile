FROM ubuntu
MAINTAINER David Glantenay

RUN apt-get update
RUN apt-get -y install apt-utils
RUN apt-get -y install python-setuptools
RUN apt-get -y install python-pip
RUN apt-get clean
RUN mkdir -p /app/auth
RUN mkdir -p /app/config
COPY . /app/auth
RUN pip install -r /app/auth/requirements.txt

ENTRYPOINT ["python", "/app/auth/manage.py", "runserver", "--host", "0.0.0.0"]