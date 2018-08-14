# Pull base image
FROM python:3.7

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN export DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get -y install build-essential curl
RUN curl -sL https://deb.nodesource.com/setup_6.x | bash -
RUN apt-get install -y nodejs
RUN nodejs -v && npm -v

# Set work directory
WORKDIR /code

# Install dependencies
RUN pip install --upgrade pip
RUN pip install pipenv
COPY ./requirements.txt /code/requirements.txt
RUN pip install -r ./requirements.txt
#RUN pipenv install --deploy --system --skip-lock --dev

# Copy project
COPY . /code/
RUN npm --prefix /code/projectmanager/static/projectmanager install /code/projectmanager/static/projectmanager