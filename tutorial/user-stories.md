# User Stories

## Introduction

[User stories](https://en.wikipedia.org/wiki/User_story) is an important mechanism for engineers to understand the functionality of their software. These can take many forms, but often include statements set-up as 
    
    As a <ROLE>, I want to <WHAT> because <WHY>.

For this tutorial, we can consider a few different roles as important:

* user (the people using Iris, the software)
* sys ops (the person who has to deploy and maintain the server)
* application support (the person that will do application support)
<!--more-->
These roles are not independent! Your sys ops and application support users may be the same person. Everyone could be users -- in fact, they could be using the ticketing system to track changes to the ticketing system, such as upgrades, plugins, custom code, etc. (John C Note: as an Atlassian Administrator for the majority of the past three and a half years, I can say that this was my life).

This document will change over time. As such, each time a user story is added the following will be created:

1) a Github issue
2) A new section labeled by Lesson that the story is attached
3) A new entry under the section for the user story that links to the Github issue.

## Why all this documentation

This is generally a bit more than an engineer would normally handle. In larger organizations, there will be a program manager or scrum lord handling ticket creation, tracking user stories, etc. However, this is being approached as "A single person setting out to change the world, one ticket at a time." From that stand-point, "we" (the royal single and the plural) are tackling all portions, and showing what it'd be like to work on a project of this magnitude (even in tutorial form). That may be overkill if you're hitting this just to learn more about the [technology stack](/docker-hug-tutorial/why-tech). 

## The Stories

### Beginning

* As a user, I can create tickets.
* As a user, I can assign tickets to other users.
* As a user, I can add descriptions, titles, and due dates to the tickets that I have permission to change.
* As a user, I can add comments to the tickets.
* As a user, I can change basic information about myself (email, phone, etc.)
* As a user, I can set my notification preferences.

* As sys ops, I can install the stack easily, effectively, and repeatedly.
* As sys ops, I can easily view all logs and identify isses that may arise. 
* As sys ops, I can make manual changes if needed to the system.
* As sys ops, I can customize the environment well enough to work with our system architecture.
* As sys ops, I can ensure the software is secure and safe for end users.

* As application support, I can maintain users (add, delete, change).
* As application support, I can see the most important issues easily and relay the information to sys ops if needed.
* As application support, I can alter any ticket.
* As application support, I can deal with any authorization issues with the software.
* As appication support, I can enable or disable notification possibilities based upon what is available on the system.