# Weekly To-do List
#### Video Demo:  https://youtu.be/TZdTYbofyso
#### Description:
A command line to do list for the week. It allows the user to see the week at a glance, a specific day, add, remove, and mark as complete. The tasks are saved on a database in sqlite. Since this is command-line based, I used argparse and parsers for easy access to the functions.

## Functions

### Overview -ov
The overview function prints out a calendar like table of the current tasks in the to-do list. It will show the tasks, along with it's status (complete or incomplete) and the time it is set for in the specific day.

### View -v day
The view function is similar to the overview function, but only shows the specified day. This was implemented so that if the user is tackling their tasks for the day, they can focus on just that day.

### Add -a
The add function allows the user to add tasks at a specific time on a specific day. It will continue prompting the user for tasks to add until the user types 'done' to indicate that they have added all tasks. The tasks are, by default, given an incomplete status.

The add function works with the day and time validation functions to ensure that they make sense.

The function also allows for the user to add the same task to everyday of the week by inputing the day as 'all', for ease of use.

After 'done', the program will print the overview so that the user can verify all their tasks have been correctly and successfully added.

### Remove -r
The remove function allows the user to remove a task if they do not want it in their list anymore. This is different from the complete function as it removed the task completely. Additionally, it allows the user to remove any tasks they might have added wrongly.

This function works with the ID validation function to ensure that the task to be removed exists.

### Complete -c
The complete function allows the user to mark a task as complete. This will change the boxmark into a checkmark.

This function works with the ID validation function to ensure that the task to be marked complete exists.

## Validation Functions

### validate_day
Using regular expressions, this validation function takes the input of the user for the day and checks if they match any day of the week or 'all'. If the day matches, the function returns True for the other functions to continute, else it returns False for the error message 'Invalid day' to be printed.

This is necessary so that when the user adds a new task, sqlite can successfully add the new task into the tasks database.

### validate_time
Using regular expressions, this validation function takes the input of the user for the time and checks if it is a valid 24h time. If the time is valid, the function returns True, else it returns False for the error message 'Invalid time' to be printed.

This is necessary so that when the user adds a new time specific task, sqlite can successfully add the new task into the tasks database and order the tasks according to the time in the day.

### validate_id
This validation functions checks the ID input by the user against the list of active ID's in the tasks database. It returns True if the ID is valid, else returns False for the error message 'Invalid ID' to be printed.

This is necessary so that when the user wants to remove or mark complete a task, the task can be successfully accessed by db.execute.

## Design choices

### Command Line Interface
I chose to do this project on the command line as it is fast and efficient. Everything can be done using the keyboard, unlike with the conventional Notes or Calendar apps.

The use of parsers make the program run even faster as it skips the middle ground of asking which function the user wants to execute after running the program.

### Usage of SQL
SQLite is used so that even if the user quits the program, their tasks are still saved. This is necessary as the user would want to see their tasks everyday, but would not want to be running the program in the background all the time.

SQL also allows for organisation of the tasks by day and time, which allows for neatness when the user is viewing their tasks.

### Usage of IDs
SQL assigns every row of data with a unique ID. Taking advantage of this, removing and marking tasks as complete using their IDs make it easier for the user as they do not have to re-type the name of the task itself. This reduces potential errors due to typos, reducing stress of the user.