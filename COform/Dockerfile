from python:3.9.1
MAINTAINER Moz Chung "mozchung@smarter.com.tw"

# Set the working directory to root
WORKDIR /app

# Copy Evertyhing into the working dir
ADD . /app

#Install dependency
RUN pip install -r requirements.txt
RUN pip install uwsgi

#run the command to start uWSGI
CMD ["/usr/local/bin/uwsgi", "app.ini"]
