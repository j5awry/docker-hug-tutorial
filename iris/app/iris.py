import hug
import sqlalchemy

@hug.get('/echo')
def echo(text):
        return text

@hug.get('/hello')
def hello():
        return "Hello from Iris, messenger of the Gods"