# Task manager 
An app to manage task completion and time management for users and groups. Leaders can give group members tasks and see their progress. Users can also create their own tasks for themselves and mark them as completed. 

Features of the application include: 
- User login and registration (x)
- User can create tasks for themselves, these are only visible for themselves and can be edited and deleted by the user
- Leaders can create groups and add users to the groups
- Leaders can create tasks for group, and only leader can delte tasks in this group
- Users can add comment to the tasks 
- Tasks can have status of completed, in progress or not started, or late 
- Leader can assign tasks to users
- Leader can see progress of group members
- Leader can set a deadline for tasks
- Leader can see how much time a task took to complete
- Leader can see how much time a user spent on tasks

Currently working features:
1. Registration, login
2. Task creation
3. Can view tasks in a list
4. Can view individual tasks
5. Leader can create a group
6. Leader can view a list of roups (this need the links to pages still)
7. Add member to group (this does not work, need debugging)
8. Leader can select group to which assign the task 
9. Edit task somehow does not work

How to use (local):
Clone the repository to your machine and move to its root folder.
Create an .env file create an .env file in the folder and set it as content:\
DATABASE_URL=postgresql+psycopg2://
SECRET_KEY=87dk98hlloiyuh
Next, activate the virtual environment and install the application's dependencies using the commands

$ python3 -m venv venv

$ source venv/bin/activate

$ pip install -r ./requirements.txt
Then run flask using command 
$ flask run 
