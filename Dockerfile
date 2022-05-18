FROM odoo:14.0

LABEL MAINTAINER PRESICION SMART SERVICES <https://pssitcorp.com/>
USER root
RUN apt-get update
RUN apt-get install -y pip-pytesseract
#RUN apt-get install -y tesseract-ocr-all