FROM python:3.6

MAINTAINER tobias.leong "tobias@data.gov.sg"

# create necessary file system
RUN mkdir /root/apps && mkdir /root/apps/data && mkdir /root/apps/app

# copy files over
COPY app/app.py /root/apps/app
ADD app/templates/ /root/apps/app/templates
COPY config.json /root/apps
COPY requirements.txt /root/apps
COPY startup.sh /root/apps
COPY app/__init__.py /root/apps/app
COPY __init__.py /root/apps
COPY wsgi.py /root/apps
COPY app/static /root/apps/app/static

# change user permissions
RUN chmod +x /root/apps/*

# setup runtime stuff
RUN cd /root/apps
RUN pip install -r /root/apps/requirements.txt

# you need this to set the PATH correctly for gunicorn to work properly
ENV PYTHONPATH "${PYTHONPATH}:/root/apps"

# run server
EXPOSE 5000
ENTRYPOINT ["/root/apps/startup.sh"]
CMD ["sudo"]
