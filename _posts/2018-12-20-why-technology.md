---
layout: post
title:  Why Technology
date: 2017-12-20
permalink: why-tech.html
order: 2
excerpt_separator: <!--more--> 
---
# Technology Explanations

In deciding to create a tutorial, I'm using a combination of technology I know (Ubuntu) and don't know (React), things I'm comfortable with (Python) and things I'm not (Hug), concepts I'm a supposed master of (SSL/TLS Certificates) and others I know little about (Docker networking). This gives me a chance to exand myself, while also providing better instructions. We can struggle together on some portions, and I can masquerade as the master in others.
<!--more-->
## Operating Systems
Currently, this is only tested on Ubuntu 16.04. I offer no guarantees on things working on other operating systems

## [Why Docker?](https://docs.docker.com/)

Docker can be a finicky beast. There are numerous ways to control the ecosystem, create networks, spin up engines, and do all the jargon. My relationship with Docker is mixed. I ran a build system that created Docker engines and pushed them to a private registry, spun up a large scale Artifactory system primarily for multiple registries (it's up to 5 production servers, a couple HA set-ups, a singleton, all using Postgresql, and replicating everywhere). I've helped others set-up Docker engines locally, tested tons of registry commands, but, well...I've been a Vagrant person for local development, and my applications haven't ever been designed as microservices, and my databases have always been separate servers due to scaling.

But Docker is the future! At least that's what my most vocal slack channel keeps telling me. Considering my company's more recent adoptions of Docker, it was probably time I got over my dislike, and dive in. So you'll get to join me!

## [Why Python, especially Python 3.6.3](https://www.python.org/)
Python 2 is [counting down to doom](https://pythonclock.org/). Also, Hug is officially only supported in Python 3. I also like staying close to latest. 

Why Python and not another language? I'm comfortable working in Python. I'm not comfortable working with Hug. Maybe I'll do implementations in other languages later. Maybe Go. I like Go. 



## [Why Hug?](http://www.hug.rest/)

Tougher question. Most of my work has been in Python. I've built a [Flask app](http://flask.pocoo.org/)(that got stuck in committee and never used), a [Django app](https://www.djangoproject.com/)(for fun), a [Click powered](http://click.pocoo.org/5/) CLI (that's used actively), and tons of other Python scripts (ranging in use from regularly to stopped working a while ago). 

As for Hug, I just built a Web API using it for a company hackathon. The site uses Hug and Postgresql, so 2 pieces of this stack. What I found was the documentation, examples, and tutorials for Hug seriously lacking. I found myself diving into Falcon documentation for specifics, and banging my head when I couldn't find an example in the [official Hug repository](https://github.com/timothycrosley/hug). I consider this a bit of giving back in a way I find to be a stronger structure

## [Why Gunicorn](http://gunicorn.org/)
**Because of the name, that's why!**

## [Why Postgresql](https://www.postgresql.org/)

I haven't worked with that many databases. MySQL and Postgresql daily for work, SQLite for some easy development, and a little Mongo and Cassandra on the side (gotta learn a little NoSQL, right?). My aforementioned Hug API may be moving to an abstracted version of Cassandra that focuses on being a key:value store. And a little time-series based work with Influx, but only enough to know that I don't really need time-series based data.

So why Postgresql? I'm somewhat familiar with the flow, I'm currently more interested in SQL based databases than NoSQL, and at least one application at work is using a Posgresql Docker engine. Might as well get more familiar with something for work. Plus, I like Postgresql far more than MySQL

## [Why React](https://reactjs.org/)

Gotta learn a front-end technology sometime. React is in vogue. Plus, I like that it's declarative.


## Why aren't you telling me what webserver you're using yet?

I haven't decided, that's why. Maybe I'll use NGinx, maybe I'll use Apache HTTPD Webserver. Or maybe something else if I decide to dig around and see what is available. Perhaps you can decide for yourself, and I just provide basic instructions! *Maybe I'll provide instructions for more than one!*

Or decide later. Probably that.

## What is Iris?

Iris was the messenger of the gods. Unlike Hermes, Iris was thought to be a bit more reliable, a bit more single minded. She was the personal messenger of Hera, and described in mythology [more directly](https://mythology.stackexchange.com/questions/1438/why-do-the-greeks-have-two-different-messenger-gods). Hopefully you just said "He copied that from his introduction!"

Iris is a ticketing system. It assigns tasks to users, emails them to inform them about the tasks, and displays all tasks, and tasks by user. There is no intention for this to replace [Bugzilla](https://www.bugzilla.org/) or [Jira](https://www.atlassian.com/software/jira), but I bet it'll be able to replace your Salesforce implementation. Ok, I jest -- I just have some issues with my company's implementation for our helpdesk.

Oh, there will probably be rainbows involved. Maybe unicorns too. Haven't decided yet.

## The Basic Ecosystem
One server or VM, Docker Engines all nicely networked. 

    Webserver
      ^   ^
      |   |
      |   |-> React
      |         |
      |---------|-> Gunicorn
                     ^
                     |->Hug
                         ^
                         |
                         |->Postgresql