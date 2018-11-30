import hug
from app import alembic
import logging
import sqlalchemy
from falcon import HTTP_404, HTTP_500, HTTP_400, HTTP_201
import collections
import os
import json


logging.basicConfig(level=logging.DEBUG)

ENGINE = sqlalchemy.create_engine(
    'postgresql+psycopg2://{}:{}@pgdb:5432/iris'.format(
        os.getenv("IRIS_USER"),
        os.getenv("IRIS_PASS")),
    echo=False,
    echo_pool=False)
SESSION = sqlalchemy.orm.sessionmaker(bind=ENGINE)


@hug.get('/tickets')
def tickets():
    logging.debug("Tickets called")
    return [{"id": 1, "title": "Our First Ticket"}]


@hug.put('/tickets')
def put_ticket(response, 
               title: hug.types.text,
               assignee: hug.types.text=None,
               due: hug.types.text=None,
               description: hug.types.text=None):
    logging.debug("Putting a new ticket")
    session = SESSION()
    new_ticket = alembic.Ticket(
        title=title,
        assignee=assignee,
        due=due,
        description=description)
    try:
        logging.debug("Attempting ticket creation")
        session.add(new_ticket)
        session.commit()
    except Exception as e:
        logging.error(e)
        session.rollback()
        message = {"code": "500",
                   "message": "something has gone wrong"}
        response.status = HTTP_500
        return message
    finally:
        session.close()
    return {"code": "201"}


@hug.get('/tickets/{ticket_id}')
def get_ticket(request, response, ticket_id):
    response_dict = collections.OrderedDict()
    session = SESSION()
    tid = ticket_id
    try:
        logging.info("Getting ticket dict for {}".format(ticket_id))
        ticket_query = session.query(alembic.Ticket)\
            .filter(alembic.Ticket.ticket_id == tid)\
            .one()
    except Exception as e:
        logging.error(e)
        session.rollback()
        message = {"status_code": "404",
                   "message": "No ticket {}".format(ticket_id)}
        response.status = HTTP_404
        return message
    finally:
        session.close()
    queryd = {k: v for (k, v) in ticket_query.__dict__.items() if k != "_sa_instance_state"}
    logging.info("Query return : %s", queryd)
    response_dict['ticket_info'] = json.loads(
        json.dumps(queryd))
    comment_dict = collections.OrderedDict()
    comment_dict['id'] = 1
    comment_dict['body'] = 'BEST.TICKET.EVER'
    response_dict['comments'] = json.loads(json.dumps(comment_dict))
    wf_dict = collections.OrderedDict()
    wf_dict["type"] = 'default'
    wf_dict["status"] = 'Open'
    response_dict['workflow'] = json.loads(json.dumps(wf_dict))
    real_response = json.loads(json.dumps(response_dict))
    logging.info("ticket information: {}".format(real_response))
    return real_response


@hug.get('/echo')
def echo(request,
         response,
         documentation: hug.directives.documentation,
         text: hug.types.text,
         anotherParam: hug.types.text=None):
    """Method that echoes provided text
    or optional second parameter.
    Providing parameters other than text or anotherParam results in a 404.
    """
    response_dict = collections.OrderedDict()
    allowed_params = ['text', 'anotherParam']
    for key in request.params:
        if key not in allowed_params:
            logging.error("incorrect param")
            response.status = HTTP_400
            response_dict['status'] = 400
            response_dict['message'] = "Incorrect Parameter supplied"
            response_dict['bad_parameter'] = key
            response_dict['usage'] = documentation
            return response_dict

    if text and anotherParam:
        logging.error('text: {}'.format(text))
        logging.error('anotherParam: {}'.format(anotherParam))
        response_dict['text'] = text
        response_dict['anotherParam'] = anotherParam
        return response_dict
    elif text:
        logging.error(text)
        response_dict['text'] = text
        return response_dict


@hug.get('/hello')
def hello():
    logging.error("Hello called")
    return "Hello from Iris, messenger of the Gods"
