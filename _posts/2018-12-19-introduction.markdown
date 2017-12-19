---
layout: post
title:  Introduction
date: 2017-12-19
permalink: introduction.html
order: 1
excerpt_separator: <!--more--> 
---

Welcome to my tutorial on Docker, Python APIs via Hug, SQLAlchemy, and Postgresql. This tutorial will walk through the creation of a Docker powered microservice webapplication called Iris. 

Iris was the messenger of the gods. Unlike Hermes, Iris was thought to be a bit more reliable, a bit more single minded. She was the personal messenger of Hera, and described in mythology [more directly](https://mythology.stackexchange.com/questions/1438/why-do-the-greeks-have-two-different-messenger-gods).

#### Using this tutorial

Each lesson resides on a branch, aptly named Lesson-N. Each Lesson has a corresponding post on this page for HTML viewing. These pages are also included in the *tutorial* directory. Note that each lesson branch contains only the tutorial directions up to that lesson. This allows for review, but not looking ahead.

The master branch is current stable and furthest along. If you're coming to this tutorial early, you'll see the master branch expand as pull-requests come in from each lesson.

#### Following along with the code

First, clone or fork [the repository](https://github.com/j5awry/docker-hug-tutorial). It'll default to the master branch. This has the code completed to this point of the project. As stated above, if you come to this early, you'll notice more lessons added, and master evolving over time. 

To look at the code for a specific lesson, follow along, or make changes, use `git checkout Lesson-(N)` to checkout the branch. Each lesson branch will work -- that's a promise.

You can also view the code using the viewer on Github if that's more your style. The use of git is not explicitly covered in this tutorial. I'm a fan of official docs, so if you've haven't used github much, head on over to their [tutorials and documentation](https://guides.github.com/)

#### Do It Yourself

The tutorial will reference the code regularly, however, there will be chances to code on your own, make additions, make changes, and end of lesson questions and thoughts. Try your best to make the requested changes or additions. The answers will be provided in the next lesson. NOTE: Some of these are challenges or questions that may not actually be good for the application. The answers may be there, but the code you wrote may not be included at all in the next lesson. This is part of the fun of coding -- you can choose to include your changes or follow my design for the application. 