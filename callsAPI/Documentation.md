# Work at olist project
This documentation explains how to run the project, some of the project's decisions and my
of what could be improved in the project.

## Executing the project
To execute this project is required the installation of the docker and docker-compose, see the
links below. <br>
Docker: https://docs.docker.com/install/ <br>
Docker-compose: https://docs.docker.com/compose/install/ <br>
To run the project execute the command: docker-compose up <br>
It will be running in localhost port 8000. Note that the port 5432 is used by the data base
and should be free.

## Project Decisions
The call was modeled as single element for the start and end record times, this decision was 
made to optimise the volume of request to the database and improve database organization 
and simplicity. This decision impacted in the implementation, since it did't allowed the 
use of model serialization because the input model was different of the database model. 
Requiring the implementation of a custom serializer and custom validation for the view. <br>
I also decided to add a field for the cost, since was informed that formula to calculate the 
cost of call could change but the calls that were already charged can not change.
With this in mind we can see that most of the processing is done when inserting a new call,
calculating the value of call and validating if that input is valid. A valid input should 
have a start smaller than an end, should not have the call_id and type of a already inserted 
record and a start record should have source and destination. <br>
This decisions made the billing endpoint very simple, since it just filters the database
by origin and period if informed and serializes it based on the database model. <br>

## Improvements
I would add more tests for weird scenarios. <br>
I would check for ways to optimise the serializer for the input. <br>
I would sanitise the unused files, but some say that is better to let the basic structure 
in case it is used in future features, so when developing with other people without a 
decision about it i don't delete the files.