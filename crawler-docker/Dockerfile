FROM ubuntu:13.04
MAINTAINER Rick Moynihan "rick.m@swirrl.com"

# install prerequisites
RUN sed -i 's/main$/main universe/' /etc/apt/sources.list && apt-get update

RUN apt-get update && apt-get clean

RUN apt-get install -y python-dev curl wget zip

RUN cd /tmp; wget http://python-distribute.org/distribute_setup.py

RUN cd /tmp; python distribute_setup.py; easy_install pip; \
    rm distribute_setup.py

RUN pip install rdflib>3.1 && pip install requests

RUN useradd -m crawler

ADD crawler /home/crawler/crawler

ADD bootstrap /home/crawler/bootstrap
ADD bootstrap.sh /home/crawler/bootstrap.sh

RUN /home/crawler/bootstrap.sh

#ADD sample-rdf /home/eldis/rdf

#CMD python /home/crawler/crawler/eldis/eldis_update.py

CMD python /home/crawler/crawler/import-data.py eldis
