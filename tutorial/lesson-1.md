# Lesson 1

## Getting Started

Time to dig in! Let's start with a little local dev information.

It's fairly standard for Python development to work in virtual environments. Docker handles this separation for us, so we don't need to use [virtualenv](https://virtualenv.pypa.io/en/stable/) or other technologies. So let's take for granted that we're going to use Docker for all the steps.

## Where do we start?

Review the why-technology.md file. That will provide background into the stack we'll be using. From there, if you haven't run through the [Docker Getting Started](https://docs.docker.com/get-started/) doc, give it a quick run. We'll be covering a lot of the same concepts, but it's good to have a little background.

[Install Docker](https://docs.docker.com/engine/installation/). As stated in the why-technology, this tutorial is written using Ubuntu 16.04. This should work on other OS's, but there is no guarantee at this time.

To make life a bit easier, [add your user to the docker group](https://docs.docker.com/engine/installation/linux/linux-postinstall/). 

Now on to creating Docker engines. We're going to start with two containers -- the Postgresql official and a container we'll build called iris. If you're not familiar with [Docker Hub](https://hub.docker.com/), pop on by, make a login, and browse. There main feature I look for in [base images](https://docs.docker.com/glossary/?term=base%20image) is officiality. If it's marked "Official", a user can be confident of maintenance, serviceability, and functionality. For Iris, let's use the official [Python Docker container](https://hub.docker.com/_/python/).

## The Dockerfile

Since we'll be building Iris, we'll need a Dockerfile. Digital Ocean has a [good write-up](https://www.digitalocean.com/community/tutorials/docker-explained-using-dockerfiles-to-automate-building-of-images) on the Dockerfile. It's also handy to keep around Docker's [best practices](https://docs.docker.com/engine/userguide/eng-image/dockerfile_best-practices/).

Iris is housed in the folder aptly named iris. The Dockerfile is simple at this point:

    FROM python:3.6.3-stretch

    EXPOSE 8000
    
    WORKDIR /var/lib/iris
    COPY . .
    RUN pip install -r requirements.txt
    CMD ["/bin/bash", "-c", "gunicorn --bind 0.0.0.0:8000 --workers 3 app.iris:__hug_wsgi__ >> logs/iris.log 2>&1"]

The breakdown:

`FROM python:3.6.3-stretch`: [FROM](https://docs.docker.com/engine/reference/builder/#from) specifies a base image (or other container) that your image is based upon. In this case, we'll be using the stable Python 3.6.3 in Debian Stretch. 

`EXPOSE 8000`: By default Gunicorn and Hug want to work on port 8000. This can be customized. [EXPOSE](https://docs.docker.com/engine/reference/builder/#expose) makes the port available.

`WORKDIR /var/lib/iris`: [WORKDIR](https://docs.docker.com/engine/reference/builder/#workdir) sets the working directory for anything that follows. 

`COPY . .`: [COPY](https://docs.docker.com/engine/reference/builder/#copy) all the files from the Dockerfile's directory to `/var/lib/iris` as defined by WORKDIR. This isn't the most clear instruction, but it's a good illustration of how WORKDIR operates in context. If you're wondering about ADD vs. COPY, check those [best practices](https://docs.docker.com/engine/userguide/eng-image/dockerfile_best-practices/#add-or-copy) again.

`RUN pip install -r requirements.txt`: [RUN](https://docs.docker.com/engine/reference/builder/#run) written as a shell command. By default, RUN will use /bin/sh. The only Python installed is Python 3.6.3. Pip is included. This will add in our dependencies (as of this time)/

`CMD ["/bin/bash", "-c", "gunicorn --bind 0.0.0.0:8000 --workers 3 app.iris:__hug_wsgi__ >> logs/iris.log 2>&1"]`: [CMD](https://docs.docker.com/engine/reference/builder/#cmd) provides the defaults for a container upon start. In this case, using `bash` call `gunicorn` to bind on `0.0.0.0:8000` with 3 workers. 

Gunicorn calls a Python program, in this case `app.iris:__hug_wsgi__.` Recall that our working directory is /var/lib/iris. After that, it's a redirect to a log file, capturing stand-err. There's a bit of logging ugliness at the moment in the application, but that will get cleaned up later. 


At this point, you could run a `docker build` and execute this single container. But let's move on a bit.

## docker-compose.yml

    version: "3.2"
    services:
      postgresql:
        image: postgres:9.6.6
      iris:
        build: ./iris
        volumes:
          - iris_vol:/var/lib/iris
        ports:
          - "8000:8000"
    volumes:
        iris_vol:

[Docker-compose](https://docs.docker.com/compose/) provides a way to spin up a series of Docker containers that work together as a single application. The [docker-compose.yml](https://docs.docker.com/compose/compose-file/) is the configuration file providing lots of information. It uses the YAML syntax. You can check YAML's official site, but I like the [Ansible page](http://docs.ansible.com/ansible/latest/YAMLSyntax.html) a bit more. Breaking it down quickly:

`version`: set the version of the docker-compose file format. See the above linked info about the docker-compose file. In this case, we're using a somewhat recent version, taking advantage of a few capabilities of version 3 (which we'll get into).

`services`: List of the docker images to use, and their specific configurations.

`posgresql: image: postgres:9.6.6`: Pull down and use the postgres:9.6.6 docker container

`iris: build: ./iris`: run `docker build` in the directory ./iris. We'll need this to build our container, since we aren't pushing it to Docker Hub (at this time).

`iris: volumes: [iris_vol:/var/lib/iris]`: 

`iris: ports: ["8000:8000"]`: [Ports](https://docs.docker.com/compose/compose-file/#ports) creates a mapping between host and container. In this case, we want port 8000 to be consistent. By default, the short syntax of `ports: ["8000"]` would result in a random host port being mapped to the Iris container's port 8000. Also note that I used array notation here, and more native YAML `-` notation in the file. Either works, but the bracket array is cleaner for a single line

`volumes: [iris_vol]` specifies a [Docker volume](https://docs.docker.com/engine/admin/volumes/volumes/). We'll spend more time on volumes later. The short version is that volumes provide a way for data to persist. Volumes are managed by Docker, not the container. They also don't increase the size of the container. In the case of Iris, the main addition is logs now being stored on the host rather than in the container

## Iris, the most minimal messenger

Iris is as minimal as it gets right now. It'll echo what is told to it, and respond with a greeting. Checkout `iris/app/iris.py` for the code. There is a little logging ugliness. This is due to how Gunicorn and Hug deal with logging. For the moment, using logging.error will print the statements to standard out, which makes it to the redirect and the log file. We'll tackle proper logging at a later time 

## Turn the key

with the docker-compose file defined, and the Dockerfile for Iris created, we can now bring up the images.

`docker-compose up --build`

## Test

Iris has no tests right now. We'll tackle that later as well. Right now, a little functional test to see it's working is enough. Try:

`curl 0.0.0.0:8000/hello`

should return

`"Hello from Iris, messenger of the Gods"`

then the echo

`curl 0.0.0.0:8000/echo?text=WillyWonka`

should return

`"WillyWonka"`

You can also see this in the logs. Docker volumes, on Ubuntu 16.04, live in `/var/lib/docker/volumes/`. You'll need to be root to check out the volume contents.

    sudo su
    cd /var/lib/docker/volumes/dockertest_iris_vol/logs
    view iris.log

Entries should look like:

    [2017-12-20 16:48:39 +0000] [5] [INFO] Starting gunicorn 19.7.1
    [2017-12-20 16:48:39 +0000] [5] [INFO] Listening at: http://0.0.0.0:8000 (5)
    [2017-12-20 16:48:39 +0000] [5] [INFO] Using worker: sync
    [2017-12-20 16:48:39 +0000] [8] [INFO] Booting worker with pid: 8
    [2017-12-20 16:48:39 +0000] [9] [INFO] Booting worker with pid: 9
    [2017-12-20 16:48:39 +0000] [12] [INFO] Booting worker with pid: 12
    ERROR:root:Hello has been called
    ERROR:root:echoed WillyWonka

## Stopping everything

Feel free to bring down the docker-compose environment. `ctrl+c` will stop docker-compose. To stop the images, run `docker-compose down` or `docker-compose stop`. If you ran any intermediate commands, you may need to stop other layers or containers. Check out what's happening with `docker ps -a`. If you see some containers hanging out that are stopped, but not gone, you can use `docker rm` to remove them. 

example:

    docker ps -a
    CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS                        PORTS               NAMES
    116702fc1142        dockertest_iris     "/bin/bash"              11 minutes ago      Exited (0) 11 minutes ago                         keen_bhaskara

    docker rm 116702fc1142

you can see what images exist on your system with `docker images`. Feel free to remove dockertest_iris and any other odd intermediate images using `docker rmi`

example: 

    docker images
    REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
    dockertest_iris     latest              8f3d251000c5        26 minutes ago      947MB
    <none>              <none>              43e2522d0898        28 minutes ago      947MB
    python              3.6.3-stretch       f3c64693da0d        8 days ago          911MB
    postgres            9.6.6               5579c7505b1b        8 days ago          268MB

    docker rmi 8f3d251000c5 43e2522d0898

## Questions and Gotchas

That's it for lesson 1. There's a lot of text here, lots of definitions. We'll start getting in to more meaty code next time. But here are some parting questions

* As stated, docker volumes persist data on the host. We specified one volume for Iris. Where is another place a volume would be valuable in this application?
* Persisting data is great. Try changing `hello()` in iris.py to a new greeting. Then run `docker-compose up --build` and then `curl 0.0.0.0:8000/hello`. Why did you get the response you did?
* What are some other containers we'll need to add to docker-compose.yml? Try identifying one or two, and adding them. (hint: you can check out the why-technology.md file to see some of where we'll be going)
