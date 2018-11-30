FROM python:3.6.3-stretch

EXPOSE 8000

WORKDIR /var/lib/iris
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
ENV PYTHONPATH="/var/lib/iris"  PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
CMD ["/bin/bash", "-c", "gunicorn --bind 0.0.0.0:8000 --workers 3 app.iris:__hug_wsgi__", ">> logs/iris.log 2>&1"]