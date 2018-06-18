FROM ubuntu
MAINTAINER David Glantenay

RUN apt-get update
RUN apt-get -y install apt-utils
RUN apt-get -y install python-setuptools
RUN apt-get -y install python-pip
RUN apt-get clean
COPY formation_docker /app/auth
RUN pip install -r /app/auth/requirements.txt

CMD ["python", "/app/auth/manage.py", "runserver"]