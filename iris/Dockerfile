FROM python:3.6.3-stretch

EXPOSE 8000

COPY . /var/lib/iris
WORKDIR /var/lib/iris
RUN pip install -r requirements.txt
CMD ["/bin/bash", "-c", "gunicorn --bind 0.0.0.0:8000 --workers 3 app.iris:__hug_wsgi__", ">> logs/iris.log 2>&1"]