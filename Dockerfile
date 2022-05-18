FROM odoo:14.0

LABEL MAINTAINER PRESICION SMART SERVICES <https://pssitcorp.com/>
USER root
RUN apt-get update
#Dependencias de la libreria pytesseract
RUN apt-get install -qq tesseract-ocr libtesseract-dev libleptonica-dev python3 python3-distutils python3-pip
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install --upgrade Pillow
RUN pip3 install pytesseract
########
RUN pip3 install paramiko
RUN pip3 install pyOpenSSL
