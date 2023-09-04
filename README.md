# Task manager 
! Currently only in local use ! \
An app to manage task completion and time management for users and groups. Leaders can give group members tasks and see their progress. Users can also create their own tasks for themselves and mark them as completed. 

Features of the application include: 
- User login and registration (x)
- User can create tasks for themselves, these are only visible for themselves and can be edited and deleted by the user (x)
- Leaders can create groups and add users to the groups (x)
- Leaders can create tasks for group, and only leader can delete tasks in this group (x)
- Tasks can have status of completed, in progress or not started, or late (x)
- Leader can assign tasks to users (x)
- Leader can see progress of group members (x)
- Leader can set a deadline for tasks (x)
- Leader can see how much time a task took to complete (x)
- Leader can see how much time a user spent on tasks (x)

Currently working features:
1. Registration, login
2. Task creation
3. Can view tasks in one page and click to see individual tasks
5. Leader can create groups
6. Leader can add tasks to groups
7. Leader can assign task to users
8. Task can be edited (name, status, description, deadline, delete task)
9. Can see time spent on task 


How to use (local):
Clone the repository to your machine and move to its root folder. \ 
Create an .env file create an .env file in the folder and set it as content:\
DATABASE_URL=postgresql+psycopg2://
SECRET_KEY=87dk98hlloiyuh
Next, activate the virtual environment and install the application's dependencies using the commands

How to use (local): \
1. clone repository to your local machine
```bash
$ git clone https://github.com/heksaani/database-application.git
$ cd database-application
```
2. create a local .env file and insert your local DATABASE_URL and own SECRET_KEY \ 
   example .env:
```
$ touch .env
```
```
DATABASE_URL="postgresql+psycopg2://username@localhost:5432/username
SECRET_KEY=92fsdf0h
````
3. Activate a virtual environment and install dependencies
```
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r ./requirements.txt
```
4. Create database schema
```
$ psql < schema.sql
```
5. Now start the flask app
```
$ flask run 
``` 

