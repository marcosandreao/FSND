#Grab the latest alpine image
FROM python:3.8-slim-buster

# Install python and pip
ADD ./requirements.txt /tmp/requirements.txt
RUN apt-get update && apt-get install build-essential -y

# Install dependencies
RUN pip3 install -r /tmp/requirements.txt
RUN pip3 install gunicorn

# Add our code
ADD . /opt/webapp/
WORKDIR /opt/webapp

# Run the app.  CMD is required to run on Heroku
# $PORT is set by Heroku
CMD gunicorn --bind 0.0.0.0:$PORT src.api:app