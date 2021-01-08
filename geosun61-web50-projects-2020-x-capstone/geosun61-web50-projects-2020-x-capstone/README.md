# Final Project

[Web Programming with Python and JavaScript](https://www.edx.org/course/cs50s-web-programming-with-python-and-javascript?source=aw&awc=6798_1607826662_a5d706f2d3a536d07c709718c6cc3821&utm_source=aw&utm_medium=affiliate_partner&utm_content=text-link&utm_term=101248_adgoal+GmbH+-+Content)

## Tasket a task manager

## Database Structure

3 tables --> User, Day, Task

#### Users data structure

| Column   | Type               |
| -------- | ------------------ |
| username | text               |
| password | varchar            |
| email    | int Auto Increment |

#### Day data structure

| Column           | Type                                       |
| ---------------- | ------------------------------------------ |
| id               | int Auto Increment                         |
| user             | ForeignKey to user table                   |
| tasks            | Many to Many relationship with Tasks table |
| date             | Date Field                                 |
| datetime_created | DateTime Field auto_now_add=true           |
| completed_tasks  | Many to Many relationship with Tasks table |

#### Task data structure

| Column    | Type               |
| --------- | ------------------ |
| id        | int Auto Increment |
| task_text | Text Field         |

### HTML pages

All **HTML** pages have a navbar made with Bootstrap, use jinja for loops and conditional statements to
display certain content.

### /login -- login_view(request), login.html

In login route I first check if the request method is POST or else. I use Django's built-in login
system to login users that are registered. When there is a POST request I first get form data then useDjango's login function to get them a session.

### /register -- register_view(request), register.html

This is the register function to register user accounts

### /logout -- logout_view(request)

Short code to logout the user out of the session. The user is then returned to the login screen.

### / -- index route -- index(request), orderBy(request,orderbyQuery), index.js, index.html,

This is the root as well as homepage route.

#### index view

Here I just initiate the first route with a homepage if someone is logged in. The index.html acts as
the homepage. You have 3 links Home, Add Tasks and Logout. The index.html shows lists of tasks with a
table listing the index loop, the Date for the task, the list of tasks and then the date it was
created. You can also delete the day whenever you want on the right side of the table there is a delete
day button. You can click on a task to complete it. On refresh you will see your changes. If user is
not logged in then I will redirect them to the login page. You can order the days and tasks by Oldest
Date, Latest Date and Created Date which is controlled by the JavaScript code which I will explain next.

#### /orderby/<str:orderbyQuery> -- orderBy(request,orderbyQuery)

This is the route called by the function orderSet in JavaScript from a fetch call. This route retrieves
all of the days and tasks made by and returns them to an object sent to the index homepage to be
displayed in the index.html page.

#### index.js

Here in index.js which is the script for the index HTML page. I created a function called orderSet()
which calls two other functions which I will explain after this in the [function.js](#function.js)
section later. orderSet takes an orderby_value from the radio button you click on and will order the
days and tasks accordingly. The days and tasks will be filled into a table created in the index.html
page.

#### index.html

In the index.html page I have a welcoming messages to show which user is logged in. After that I have
three radio buttons for the user to click on to see how he wants his tasks to be ordered by. The three
radio buttons are controlled using javascript onclick events as explained in the [index.js](index.js)
section above. After that I have a div for the days and tasks. Inside the div I have the table that the
days and tasks will be loaded into. The table will have the index loop, the day the tasks are going to
be completed, the list of tasks, the date it was created, and then the delete button.

### /add -- add route -- add_tasks_view(request), addtask.js, addtask.html

This is the route to add a day and tasks

#### add_tasks_view(request)

In the add route on GET requests I load an HTML page with a form for users to enter what day and tasks
they want to add for that day. In the POST requests received from this form I check if the day exists,
if it does I return an error saying the day already exists. If the day does not exist I get the data
then extract the date and tasks. I run a for loop to check if the tasks exist or not. If the task(s)
exists then I retrieve from the database if not then I create the task(s). After that I append all
task(s) to an array and then I add them to the new date and return a 200 status.

#### addtask.js

On the loading of the add task html page you will see a form for a date and one task. You will also see
2 buttons one "Add Tasks" and "Save" button. I run two JS functions here which I will explain them
later in functions.js section. The "Add Tasks" button allows the user to add more than one task for the
date you enter in the field. The button is setup at the top with the onclick event listener which adds
more tasks text fields. Then I setup an onclick event for the submit tasks form. On submit I get the
data from the date field and tasks field. In the submit tasks onclick event I check for errors in the
submitted array. I check for if the user enters the date or task and if the user already has an entry
for the date entered.

#### addtasks.html

This is the html page for adding tasks, it has a form to enter the date and tasks and two buttons
explained in the previous sections for adding tasks. The first button is "Add a Task" which allows the
user to add more task inputs to enter however many they so choose. The second button is to submit the
tasks and day and save it to the database.

### /completetask/<int:day>/<int:task> -- complete_task(request, day, task), completedTask(day_id,task_id)

This is the route to complete a task.

#### complete_task(request,day, task)

When a task is complete, users are able to click on a task and cross it off. On the event that a user
clicks on a task the python code is setup to add the task to the completed_tasks field in the Day
object. The tasks is added or removed depending on if the task was originally completed or not. It is
added or removed to/from the Many to Many relationship in the Day database table's completed_tasks
field.

#### completedTask(day_id,task_id)

An onclick event is setup and calls this function completedTask and takes two parameters a day_id and
task_id. It takes the day object id and task object id and puts it into a fetch function to setting the
task complete.

### /delete/<int:day_id> -- delete_day(request, day_id), deleteDay(day_id)

This is the route to delete a day object.

#### delete_day(request, day_id)

This view function in views.py deletes a day object by taking the day id. It is activated when a user
clicks on the delete day button on the right side for the Day object in the day and tasks table.

#### deleteDay(day_id)

This is a short fetch function in functions.js to send a PUT request to delete the day in the Day
database table.

### function.js
### -- add_task_input(parentid), submit_tasks(task_class, date_id), createTasks(arr), orderSet(orderby_value), setTable(days_obj), orderBy(orderbyQuery)

The function.js file holds most export export functions to keep the main js files (addtask.js and
index.js) from being cluttered.

#### add_task_input(parentid)

Used in [addtasks.js](#addtask.js) it is used in the onclick event for the Add Tasks button. It takes
in the parentid for the div. After it creates an text input element with classes 'form-control tasks'
and appends it as a child to the div.

#### submit_tasks(task_class, date_id)

This is the second function also used in [addtasks.js](#addtask.js). The function is used in the
addtasks.js file to save the entered date and tasks and save them to an array.

#### createTasks(arr)

This is the last function from function.js called in [addtasks.js](#addtask.js). It is called when the
error check is done, it takes the array returned from the submit_tasks function. The array is used in
the function to send the date and tasks to the /add route using a fetch function with a POST request.

#### orderSet(orderby_value)

The function orderSet uses orderBy(orderby_value) and setTable(days) to setup the table data and
features in the [index.js](#index.js) file. Firstly, I get the results of the orderBy object of days
and tasks. Secondly, I set all the table elements with the setTable function. After I set the tasks
with an onclick event for them to be completed with completedTask(day_id, task_id). In the onclick
function for the tasks I first retrieved the class get the dataset values for the day and task ids.
Once the day and task ids are set then I check if the attribute "checked" is set to true or false. If
true the task will be removed from completed tasks, else the task will be added if "checked" attribute
is set to false. The last feature for the table of days and tasks is the delete day button which is
setup in this function. For this feature I get the button class then set an onclick event. In the
onclick event I get the day id value and send a JavaScript confirm() function to ask if the user wants
to delete the day or not. If they click the OK button in the prompt the day will be deleted, else if
they click the Cancel button the day will not be deleted.

#### setTable(days_obj)

The setTable JavaScript function takes in the days object from the orderBy function and sets the table
with all of the elements for the [index.html](#index.html) page.

#### orderBy(orderbyQuery)

This function takes the order by value from the radio button click and sets the days and tasks
accordingly. It uses a fetch function to the orderby route and returns the days objects.  
