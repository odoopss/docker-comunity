FROM odoo:14.0

LABEL MAINTAINER PRESICION SMART SERVICES <https://pssitcorp.com/>
USER root

#RUN apt-get update && \ apt-get -y install sudo
RUN apt-get update && \
    apt-get install \
        pytesseract \