import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

BASE = declarative_base()


class Ticket(BASE):
    __tablename__ = "tickets"
    ticket_id = sqlalchemy.Column(sqlalchemy.Integer,
                                  primary_key=True,
                                  autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    assignee = sqlalchemy.Column(sqlalchemy.String)
    created = sqlalchemy.Column(sqlalchemy.String)
    due = sqlalchemy.Column(sqlalchemy.String)
    description = sqlalchemy.Column(sqlalchemy.String)
