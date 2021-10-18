FROM python:3.6

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

COPY . /plate
RUN pip install --upgrade pip
RUN pip install -r /plate/requirements.txt
