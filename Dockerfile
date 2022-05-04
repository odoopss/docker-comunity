FROM odoo:14.0

LABEL MAINTAINER Angel Asencios <am.angell98@gmail.com>
USER root
RUN pip3 install watchdog
# RUN pip3 install pandas
# RUN pip3 install numpy
# RUN pip3 install beautifulsoup4

