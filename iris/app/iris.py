import hug
#import sqlalchemy
import logging
from falcon import HTTP_404, HTTP_500
import collections


@hug.get('/tickets')
def tickets():
    logging.error("Tickets called")
    return [{"id": 1, "title": "Our First Ticket"}]


@hug.get('/tickets/{ticket_id}')
def ticket(request, response, ticket_id: int):
    response_dict = collections.OrderedDict()
    if ticket_id == 1:
        logging.error("Ticket dict for {ticket_id}".format(**locals()))
        response_dict['id'] = 1
        response_dict['title'] = "Our First Ticket"
        response_dict['assignee'] = None
        response_dict['created'] = "Today"
        response_dict['due'] = "Tomorrow"
        comment_dict = collections.OrderedDict()
        comment_dict['id'] = 1
        comment_dict['body'] = "BEST.TICKET.EVER"
        response_dict['comments'] = [comment_dict]
        wf_dict = collections.OrderedDict()
        wf_dict["type"] = "default"
        wf_dict["status"] = "Open"
        response_dict['workflow'] = wf_dict
        return response_dict
    else:
        logging.error("No ticket by id {}".format(ticket_id))
        response.status = HTTP_404
        return HTTP_404


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
