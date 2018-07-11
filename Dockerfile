FROM ubuntu:latest
MAINTAINER Hadrien Negros "sorgenh@gmail.com"
ENV HTTP_PROXY=http://proxypac.edf.fr:3128
ENV HTTPS_PROXY=http://proxypac.edf.fr:3128
RUN echo 'Acquire::http::Proxy "http://proxypac.edf.fr:3128";' >> /etc/apt/apt.conf.d/proxy
RUN echo 'Acquire::https::Proxy "http://proxypac.edf.fr:3128";' >> /etc/apt/apt.conf.d/proxy
RUN apt-get update -y
RUN apt-get install -y python3.6 python3.6-dev python3-distutils build-essential wget
RUN echo "http_proxy = http://proxypac.edf.fr:3128" >> /etc/wgetrc
RUN echo "https_proxy = http://proxypac.edf.fr:3128" >> /etc/wgetrc
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3.6 get-pip.py
COPY . /app
WORKDIR /app
RUN pip install --proxy http://proxypac.edf.fr:3128 -r requirements.txt
ENTRYPOINT ["python3.6"]
CMD ["app.py"]