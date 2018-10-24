FROM python:3.6
MAINTAINER tobias.leong "tobias@data.gov.sg"

# create necessary file system
RUN mkdir /data

# copy entire directory over
COPY * /
COPY /app /app/

# change user permissions as per Nectar req
RUN chmod g+rwx .

# setup runtime stuff
RUN cd .
RUN pip install -r requirements.txt

# run server
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "--bind", "0.0.0.0:5000", "-t", "9000", "wsgi"]
