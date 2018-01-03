import hug
import sqlalchemy
import logging


@hug.get('/echo')
def echo(text):
    logging.error(text)
    return text


@hug.get('/hello')
def hello():
    logging.error("Hello called")
    return "Hello from Iris, messenger of the Gods"
