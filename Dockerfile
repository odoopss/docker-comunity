FROM odoo:14.0

LABEL MAINTAINER PRESICION SMART SERVICES <https://pssitcorp.com/>
USER root
RUN apt update
RUN apt install curl python3-pytesseract nano -y