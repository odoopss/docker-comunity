FROM nginx:latest
USER root
RUN apt-get update && \ apt-get -y install sudo
#RUN apt update
RUN apt install nano apt-utils certbot python-certbot-nginx -y
