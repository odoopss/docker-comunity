FROM odoo:14.0

LABEL MAINTAINER PRESICION SMART SERVICES <https://pssitcorp.com/>
USER root
RUN apt-get update
#RUN apt-get install -y PIP pytesseract
RUN apt-get pip3 install pytesseract
#RUN apt-get install -y tesseract-ocr-all