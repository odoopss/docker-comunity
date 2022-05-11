FROM odoo:14.0

LABEL MAINTAINER PRESICION SMART SERVICES <https://pssitcorp.com/>
USER root

#RUN apt-get update && \ apt-get -y install sudo
RUN pip3 install watchdog
RUN pip3 install paramiko
RUN pip3 install pyOpenSSL
RUN pip3 install pandas
RUN pip3 install numpy
RUN pip3 install beautifulsoup4

