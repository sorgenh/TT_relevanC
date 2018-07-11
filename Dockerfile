FROM ubuntu:latest
MAINTAINER Hadrien Negros "sorgenh@gmail.com"
RUN apt-get update -y
RUN apt-get install -y python3.6 python3.6-dev python3-distutils build-essential wget
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3.6 get-pip.py
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python3.6"]
CMD ["app.py"]