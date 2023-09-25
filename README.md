# ChallengeEdMachina
REST API For a hiring challenge 

##  This API has the folowing endpoints:

### GET /leads/?skip=int&limit=int
Show all leads, skiping the amount specified and up until the limit specified (i.e pagination) 
The data showed by this endpoint is an abridged version of the data of one lead, only showing lead name, last name and career

### GET /leads/{id}
Shows full data of the lead with matching _id_, if it exists on including all course attempts. If it does not exist, a 404 will be returned

### POST /leads/
Creates a lead, requires the followwing information on the request:
* name: string
* last_name :string
* carreer: string
* registration_year: int

And it can take some optional information
* email: string
* phone: string
* attempts: \[Attempts] 

The Attempts are formated in the following way:

 * attempt_year: int
 * course_name: string

If a course with that name (case insensitive) doenst exists, it will be created with no other data

The response will return the same lead object, with its database id
### DELETE /leads/{id}

Deletes the lead with matching _id_. If it doesn't exists, a 404 will be returned

### GET /courses/

Show all courses

### POST /courses/
Creates a course, requires the following information on the request
* name: string

If a course with that name (case insensitive) already exists, a 409 (conflict) Exception will be returned. Otherwise the response will return the same course object, with its database id

### DELETE /courses/{id}

Deletes the course with matching _id_. If it doesn't exists, a 404 will be returned

## Running 

The whole project is containerized, so to run it the only thing to do is be on the main project folder and run:
 
``` docker-compose up build ```