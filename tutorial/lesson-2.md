# Lesson 2: Gimme a Hug

With the basic framework out of the way, and user stories available, it's time to start looking at how to structure the application, and add some endpoints. Let's start with a little design based on the user stories. You can follow the link to the online docs or open the user-stories markdown in the tutorial directory. 

## End points

At this point, it's important to think of what [collections](https://en.wikipedia.org/wiki/Collection_(abstract_data_type)) we may need. Judging from the user stories at the beginning, there are at least 3:

1) tickets
2) users
3) administration

The tickets collection contains tickets, and their information (and possible sub-collections within tickets). Users is a collection of users and their information. Administration is a bit ambiguous, but there are stories for application admins to see information about the the application easily, as well as control various parameters. That functionality is logically separate from tickets and users, so having it's own collection (and probably sub-collections or stores) is important.

This is a short, straight-forward [document regarding API design](http://restful-api-design.readthedocs.io/en/latest/intro.html) that is helpful. Also, it can be helpful to look at other APIs. John C. has worked as an Atlassian administrator for multiple years, and has lots of experience using the APIs in most of their products. Here's a [link to their developer docs](https://developer.atlassian.com/docs/). We'll use similar endpoints for tickets and users:

    /tickets
    /users

We won't worry about administration right now. 

When working on the URIs, it important to follow an easy scheme. Iris will stick with the following:

* plural names for collections, sub-collections, or stores (if something will return more than one possible resource)
* singular names for a document (such as a single ticket)
* verbs for methods (without exposing HTTP methods. Meaning, no `/users/{username}/delete`, but instead a DELETE call to `/users?name={username}` or something similar)
* a logical CRUD mapping. Ex: There will be a table, users. hitting `/users` will return that table. To constrain that table, we should pass a parameter to the URI, `/users?name=johndoe` would return the info represented under `/users`.

This leads to an interesting question of "What is returned in each endpoint? Will `/users?name=johndoe` be different than `/users/johndoe`?"


## What's in a user?

Let's keep it simple based on the user stories:

* Name
* Username (must be unique)
* Email
* Phone (optional)
* Notification

These are all fairly standard, with phone being possibly the only interesting bit (just in case we want to set text messaging at a later date). There may be additions later, such as integrations with chat engines (which may require usernames for those services being provided).

## User Collections and Subcollections

`/users` returns a list of all users. What should it return? Consider a few factors:

1. `/users` may return an increasingly large list
2. Developers calling `/users` may not need all information about a user

For now, let's separate the concept of `/users` and `/users/{username}`. This means the information returned from each should be different. Let's constrain `/users/` to returning the minimum amount of information useful: username and email. `/users/{username}` will return everything. This defines:

* `/users` returns a list of all users. each entry is a dictionary container username and email
* `/users/username` returns a dictionary of all user information

## What's in ticket?

Looking at the user stories, we can break down a few points:

* Title
* Assignee
* Description
* Created Date
* Due Date
* Comments
* Workflow

The first six are fairly straightforward. Workflow is a different beast entirely. For those used to ticketing systems, you'll note that there are often different workflows. Sometimes tickets can freely choose their worflow, other times workflows are tied to some other specification such as a Project in Jira (well, there's a bit more to it). At this time, we're not specifying any groupings -- this software is agnostic rather than being tied to Agile software methodology (or any tech field).

## Tickets Collections

`/tickets` is defined as an endpoint specifically for retrieving tickets. Since we're beginning, let's have it run the expensive query of _all tickets_. That would obviously be incredibly expensive later on, but to start, it gives us a place. However, it shouldn't return all information. Let's add a new point to the design to help sorting and returning:

* ID

Since we're not creating a concept of projects, that should be enough to constrain and provide easy sorting. This defines the following:

* `/tickets` will return a list of all tickets. Each entry is a dictionary containing ID, Title, Created Date, Due Date. The dates allow sorting within tickets itself (ex: `/tickets?sortBy=createdDate` would return all tickets sorted by most recently created first). Default sort should be by ID, descending

* `/tickets/id` will return a dictionary with all information about a ticket.

## What's it mean in code?

Now the fun part! If you've worked with other frameworks in Python, such as Flask or Django, recognizing [routing in Hug is simple](http://www.hug.rest/website/learn/routing). Hug utilizes decorators before each method to associate routes and other information. This is viewable in Lesson 1:

    @hug.get('/echo')
    def echo(text):
        logging.error(text)
        return text

`@hug.get('/echo')` defines the method (GET) as well as the route ("/echo"). Hug automatically passes parameters as keyword arguments to the function. This means with little additions, we can quickly add new parameters:

    @hug.get('/echo')
    def echo(text, anotherParam):
        logging.error("echo called with text={text} and anotherParam={anotherParam}".format(**locals()))
        return (text, anotherParam)

Try spinning up the containers and running `curl 'http://0.0.0.0:8000/echo?text=Hello&anotherParam=World'` What did you get?

## Did it work?

If you recall the question at the end of Lesson 1, you may have already figured this one out. Remember how Docker volumes persist data? On a rebuild with `docker-compose up --build`, it doesn't copy the new code to the volume. This is expected behaviour. Docker volumes don't replace files on build -- that'd make persistence a little difficult if you build with an empty directory (like Iris does with app/logs). We'll look a bit more at the architecture of the Docker set-up soon, but for now, let's take the the easy way out. 

`docker volume ls` will show all volumes. Make sure all containers for docker-hug-tutorial are down with `docker-compose down`. Then run `docker-compose volume prune`. This command removes any volumes not currently in use. *NOTE* This could be a bit dangerous in a production environment! If you want to remove one at a time, use `docker volume ls` to get the information, then `docker volume rm <VOLUMES>` to remove one or more volumes.

After removing the offending volumes, you can run `docker-compose up --build`.

## Back to Hug

Let's examine `/echo` as it is in the code. There's a number of changes from Lesson 1. Starting with the function definition

    @hug.get('/echo')
    def echo(request,
         response,
         documentation: hug.directives.documentation,
         text: hug.types.text,
         anotherParam: hug.types.text=None):

Breaking down the syntax: `@hug.get('echo')` is a decorator provided by Hug for routing. It wraps the echo function with the HTTP Interface provide by Hug, and defines it as a `get` HTTP method. In the function definition, there are some Hug reserver keywords. `request` and `response` correspond to the Falcon [Request and Response objects.](http://falcon.readthedocs.io/en/stable/api/request_and_response.html).

`text` is the first passable parameter. `documentation: hug.directives.documentation` is a fun work around to ensure the auto-generated Hug documentation gets passed down into the function. Finally `anotherParam=None` sets a default for an optional parameter. Hug uses introspection to generate documentation automatically. It will take the provided parameters in the function (`text`, `anotherParam`), as well as the docstring, and generate JSON formatted documentation. There is an example of using this documentation in an error return message on line 50

    response_dict['usage'] = documentation

Next, there is a quick trick for validation. Hug does not have a built in way to deal with "optional" parameters right now. All parameters listed in the function definition are required. The work around is to set a default for a parameter, such as with `anotherParam: hug.types.text=None`. However, nothing stops users from passing arbitrary parameters either. A quick test shows this:

    @hug.get('/echo')
    def echo(request,
         response,
         documentation: hug.directives.documentation,
         text: hug.types.text,
         anotherParam: hug.types.text=None):

         return(request.params)

    # Curl test
    curl 'http://0.0.0.0:8000/echo?text=Hello&notAParam=StillHere'

    {"text": "Hello", "notAParam": "StillHere"} 

So a quick validation step is added:

    allowed_params = ['text', 'anotherParam']
    for key in request.params:
        if key not in allowed_params:
            logging.error("incorrect param")

Not the most elegant, but for the moment it will enforce only text and anotherParam being added. Aftwards, it an [OrderedDict](https://docs.python.org/3.6/library/collections.html) is created to enforce order of the response messages. 

## Ticket Endpoints

This leaves us the barebones of the ticket endpoints. There's a lot of lines for not a lot happening: in `/tickets` a response of a list of dictionaries is returned. In this case, a single dictionary with ticket id 1 is provided. 

`/tickets/{ticket_id}` shows how Hug (and Falcon) can deal with templating routes. By using the single curly brace and a variable name, Hug will assign the value of that point in the path to the variable `ticket_id`. Specified in the function defintion is `ticket_id` being an int. This is only a test endpoint, so an OrderedDict is created and returned. Anything request that is not `ticket_id == 1` returns a 404. 

## Exercises/Thoughts/Questions

* The `/users` endpoint has not been defined yet! Guess I got too busy at work. Could you take care of that for me?
* `/users/username` is also missing. Try creating this function, being sure to pass `username` as a variable.
* Logging is coming up soon. Think about how you'd implement a logger for Docker
* The volume scheme isn't working out too well. What changes would you make?