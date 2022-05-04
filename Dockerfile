FROM odoo:14.0

LABEL MAINTAINER Angel Asencios <am.angell98@gmail.com>
USER root
RUN sudo pip3 install watchdog
RUN sudo pip3 install paramiko
RUN sudo pip3 install pyOpenSSL
# RUN pip3 install pandas
# RUN pip3 install numpy
# RUN pip3 install beautifulsoup4

