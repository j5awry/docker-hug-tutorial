# Lesson 3 : Hook It Up!

## Updating docker-compose

Let's move into a connected world, one where Postgresql is available. I'll start by updating docker-compose.yml. Almost like I let this sit for a while...

    version: "3.6"
    services:
      pgdb:
        build: ./postgres
        volumes:
          - postgres_vol:/var/lib/postgresql/data/
        environment:
          POSTGRES_USER: iris
          POSTGRES_DB: iris
      iris:
        build: ./iris
        volumes:
          - ./iris/app:/var/lib/iris/app
        ports:
          - "8000:8000"
        environment:
          IRIS_USER: iris
          IRIS_PASS: ${IRIS_PASS}
        depends_on:
          - pgdb
    volumes:
      postgres_vol:

First, we're removing the named iris volume. Named volumes are great for perpetuating data, like with our database. But they're not so great for development! Instead, we're going to use docker-compose's relative path to mount the iris app dir into /var/lib/iris/app. This allows us to mount a local directory as a volume, and not persist data between builds. If you followed earlier setups, made changes, and didn't see the changes, that's why! Before going further, might as well clean everything up

    docker-compose down
    docker rmi <previous built images>
    docker volume prune (Note, this will kill any unused volumes. If you're working on other things, you might want to use [docker volume rm](https://docs.docker.com/engine/reference/commandline/volume_rm/#extended-description))

Next, you'll notice a couple of environment stanzas. These create environment variables in the containers when running `docker-compose up`. I'm being extremely original with my names for user and database name. 

Under iris you'll see ${IRIS_PASS}. docker-compose allows for environment variable expansion, thus allowing you to pass your environment variables into a container! Neato! In this case, I'm setting the password iris will use to connect to the db (eventually).

Now let's chat about the Postgresql image. There's some good documentation about the Postgres setup with Docker in [the official docs](https://docs.docker.com/samples/library/postgres/). Of note are the environment variables, and what they do for Postgres's container on creation. First, setting `POSTGRES_USER` not only sets the user that the container uses for postgres interaction, it also automatically creates the user if not present, _and_ creates a database named `POSTGRES_USER` with full privileges. That saves us a setup step! It also makes `POSTGRES_DB` redundant, but it's helpful to show the variable here (in case you wish to use a different database).

`depends_on` is an important addition to iris. This tell docker-compose to setup a network between the two containers. The Postgresql container defaults to listening & exposing 5432 (as all Postgresql does), so any communication from iris to postgresql will need to use that port. 

Drilling down a level, you'll surely have noticed the new directory, postgres. This contains a minimal Dockerfile and initdb.sql. The Postgres container has another really neat feature -- any sql script in `/docker-entrypoint-initdb.d/` will get run, in `ls` order, as an initialization step! This means that, on creation, you can have it execute .sql commands. For this intro to hooking things up, I'm only providing the "ticket" table. 

    CREATE TABLE tickets (
    ticket_id serial,
    title text,
    assignee text,
    description text,
    created timestamp default now(),
    due text
    );

Things to remember:
1. using the `POSTGRES_USER` environment variable, `psql` actions will be executed by that user
2. using the `POSTGRES_DB` environment variable ensures the commands are run on that database (though if you just have a user, it defaults to using the database named after the user)

That means executing this arbitrary bit of SQL will create the tickets table under the iris database. We're keeping the basic structure:

* ticket_id : an auto-incrementing serial
* title : free text field
* assignee : free text field
* description : free text field
* created : timestamp (not really being set now)
* due : text (should really be a timestamp)

## Integrating Postgresql (minimally)

Now we have a table, we should probably have a way to get tickets in. Can't show what we don't have. We're using SQLAlchemy, an ORM (Object Relational Mapper), to interact with Postgresql. Skipping finer points (and good practices), let's start with the bare minimum: getting a connection up:

    ENGINE = sqlalchemy.create_engine(
    'postgresql+psycopg2://{}:{}@pgdb:5432/iris'.format(
        os.getenv("IRIS_USER"),
        os.getenv("IRIS_PASS")),
    echo=True,
    echo_pool=True)
    SESSION = sqlalchemy.orm.sessionmaker(bind=ENGINE)

That creats an engine that connects to our Postgres database using the same hostname as the `depends_on` section of iris' docker-compose stanza. `IRIS_USER` and `IRIS_PASS` are pull from the environment. If they're not set, bad things will happen -- you'll get `None` values which won't translate. `echo` and `echo_pool` just dumps more information to the logger for our initial work. After creating the engine, we can start a session using sessionmaker. At this point, we have the basic integration done.

## ORM -- Creating Our First Object
With SQLAlchemy you model the tables (and views and other db objects) with Python objects. Due to laziness, I suggest using the [declarative base](http://docs.sqlalchemy.org/en/latest/orm/extensions/declarative/api.html). This allows for a quick style of modeling using class attributes. You can see the first model in alembic.py. Yes, I'm being a bit cutesy for no reason. This isn't strictly an [MVC pattern](https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller), but these are models. Inside alembic.py, you'll see the model for a Ticket. Ticket contains the attributes we listed earlier: ticket_id, assignee, etc. 

Each attribute relates to an SQLAlchemy type, Columns, which then refers to another type, Integer, Text, etc. These relate to the DBAPI (database API) objects, and the types available in the database itself. SQLAlchemy provides some base types to help out. Other attributes can be listed as well. Ticket_id is listed as the primary key and autoimcrements. Autoimcrement lets SQLAlchemy know that it's not going to need to worry about setting ticket_id.

## Ticket Creation

Let's add an endpoint for creation. Rather than create a new path, we can use a different method to a known path. `tickets` is being used to pull _all_ tickets, so let's reuse it for adding/updating tickets. 

    @hug.put('/tickets')
    def put_ticket(response, 
                   title: hug.types.text,
                   assignee: hug.types.text=None,
                   due: hug.types.text=None,
                   description: hug.types.text=None):

using `@hug.put('/tickets')` let's Hug know that any PUT commands to tickets should use this function. The function, `put_ticket` takes the following possible values, either via parameters, or a data upload (such as JSON).
    
* title
* assignee
* due
* description

Note it does not take ticket_id nor created. These two fields will be generated by our application, not users. 

After that, there are some try:except:finally loops. Some, like the close, normally aren't required, but this is being extremely defensive (from a bad past experience). There's logging to let us know what's happening, and a return message.  

Now, you can use a simple request (however you'd like) to add a ticket!

    curl -X PUT -H "Content-Type: application/json" -d '{"title": "A new ticket", "assignee": "jchittum", "description": "Get this done ASAP"}' 0.0.0.0:8000/tickets

## Take The Changes

Well, you'll be able to once you take the changes! With mounting a volume from a directory into a container, the code changes will be there. However, you'll need to restart the container for it to take effect. Check out the docker-compose documentation for restart options, but I've personally been using

    docker-compose down
    docker-compose up

Mainly because I end up doing some other stuff in between as well (there's always something I see before running up).

# Get The Ticket!

Drop down to `ticket` and you'll see the SQLAlchemy session getting called and simple queries. [SQLAlchemy uses a query syntax that is a little tricky at first](https://docs.sqlalchemy.org/en/latest/orm/tutorial.html#querying).

    ticket_query = session.query(alembic.Ticket)\
        .filter(alembic.Ticket.ticket_id == tid)\
        .one()

This query is interacting with the model alembic.Ticket, which relates to our tickets table. The filter used is analogous to `WHERE` in SQL. In SQL, this query would be:

    select * from tickets where ticket_id = tid limit 1;

SQLAlchemy has the ability to do complex queries, including all your favourite joins, complex filtering, order by statements, and more. Query objects are iterable, returning each instance, specifically queried column, and more. This can get a bit confusing, [so check out the docs](https://docs.sqlalchemy.org/en/rel_1_2/orm/tutorial.html#querying). Because of the combination of filter and `.one()`, `ticket_query` is an instance of the Ticket class. To create a jsonyfiable collection, I'm using an ugly little dictionary comprehension for the moment. Like most things at this point, this is far from optimal -- we're just trying to get some sort of output!

## What's next

There's only one table in the database. Well, that's a problem, as there should be several more. And what about posting comments to tickets? And those pesky workflows? 

Try making your own comment table with the initdb.sql script, creating a declaritive class, creating a post comment endpoint, and adding in the comment query to the get ticket info. Add in a new feature! 