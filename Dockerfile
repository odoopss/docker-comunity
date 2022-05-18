FROM odoo:14.0

LABEL MAINTAINER PRESICION SMART SERVICES <https://pssitcorp.com/>
USER root

#RUN apt-get update && \ apt-get -y install sudo
RUN apt-get update && \
    apt-get install \
        python3-paramiko \
        python3-pyOpenSSL \
        python3-pandas \
        python3-numpy \
        python3-beautifulsoup4 \
        python3-pytesseract \