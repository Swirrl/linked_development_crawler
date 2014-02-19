FROM ubuntu:precise
MAINTAINER Rick Moynihan "rick.m@swirrl.com"

RUN echo deb http://archive.ubuntu.com/ubuntu precise universe >> /etc/apt/sources.list
RUN apt-get update && apt-get clean
RUN apt-get install -q -y python-pip

RUN pip install rdflib>3.1

RUN useradd -m crawler

ADD crawler /home/crawler/crawler

ADD bootstrap /home/crawler/bootstrap
ADD bootstrap.sh /home/crawler/bootstrap.sh

RUN /home/crawler/bootstrap.sh

CMD /home/crawler/crawler/eldis/eldis_crawl.py
