FROM odoo:14.0

LABEL MAINTAINER PRESICION SMART SERVICES <https://pssitcorp.com/>
USER root
RUN apt-get update
#RUN apt-get install -y PIP pytesseract
RUN apt-get install -qq tesseract-ocr libtesseract-dev libleptonica-dev python3 python3-distutils python3-pip
RUN pip3 install pytesseract
#RUN apt-get install -y tesseract-ocr-all