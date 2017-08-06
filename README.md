[![Build Status](https://travis-ci.org/amritanshu-pandey/hivery-challenge.svg?branch=master)](https://travis-ci.org/amritanshu-pandey/hivery-challenge)

# API Endpoints
| HTTP Method | URL | Action |
| --- | --- | --- |
| GET | http://[hostname:port]/paranuara/company/[company_name] | Retrieve list of all employees of the company |
| GET | http://[hostname:port]/paranuara/person/[person_name] | Provide a list of fruits and vegetables person likes |
| GET | http://[hostname:port]/paranuara/people/?person1=[person1]&person2=[person2] | Given 2 people, retrieve information of both people and the list of their friends in common which have brown eyes and are still alive.  |

# How to Install
1. Pull Docker image 
    - `docker pull amritanshu16/hivery-challenge`
2. Run docker container 
    - `docker run [--name <any_name>] -p <local_port>:5000 amritanshu16/hivery-challenge`
3. API would now be accessible on local port specified in previous command

# To-Do
1. Add test cases for all end points
2. Improve excpetion scenarios for different endpoints 