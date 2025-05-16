# TooliE
#### Video Demo: [TooliE](https://youtu.be/8uBbAGHPB8E)

## What TooliE is
####
TooliE is a tool management system for a workplace which requires multiple people to work on the same tools. There are two different kinds of users in the TooliE system - a manager and an employee. 

An employee has access to three basic features only. They are, booking a tool, seeing their booked slots, and seeing the history of their bookings. The manager has access to more features than an employee does due to their need of overseeing tool usage in the workplace. On top of the same features as the employee, a manager can view the timesheet of tools being used by all employees as well as the history of all employees. Additionaly, the manager can register new employees and see a list of current employees they have. 

## What each file of the project contains and does 

### 1. Static folder : Contains styles.css
#### This file, as it's name suggests is responsible for the basic styling of the html pages.

### 2. helpers.py : Contains helper functions 
####
The first helper function is login_required. This function is needed to ensure certain functions and pages are only accessed by a user who is logged in. 

The second and third helper functions are get_db and close_db. This function makes it easier to connect and close the database anytime I need to search or commit anything into the database. 

The fourth helper tool is formatting the time for my timeslot selection for tool booking.

### 3. SQLite Local.session.sql: Contains my tables in the database, system.db
####
My database has 3 tables - users, bookings, and history. 

#### <ins>Users</ins>
##### 
This table stores all the users who are registered in TooliE. It has 4 fields - *id, username, user_id, and password_hash*. The username is for easy identification for the manager. When seeing the list of employees, the manager can see their name and user ID. The user_id is used for logging in, and to make it easier for account recognition. For security reasons, the password is not stored as itself but hashed.  

#### <ins>Bookings</ins>
#####
This table stores all the upcoming bookings. It has 5 fields - *id, user_id, tool_name, date, and timeslot*. This ensures that anytime a user books a tool, the system knows who booked which tool for when.

#### <ins>History</ins>
##### 
Similar to bookings, this table contains the *same 5 fields plus one more, namely status*. This ensures that completed or deleted bookings can be seen by the user. 

### 4. app.py: Contains all my routes 
####
This file is the brain of the project. It contains all the necessary routes for the programme to know which page to go to. Here is the detailed breakdown of all the routes and html pages 

#### a. <ins>/managerhome and /employeehome</ins>
##### 
These routes direct respective users to their respective homepages. The difference between the 2 pages can be seen in the home page and the toolbar. As for the homepages, they are designed in **_managerhome.html_** and **_employeehome.html_**. In the manager's home page, they have quick access to booking a tool, viewing the timesheet, and registering a new user. They also have account management which is either changing their own password or viewing the list of employees they have. In the employee's homepage, they have quick access to booking a tool, viewing their bookings, and seeing their history. 

As for the toolbar, the differences are coded in **_layout.html_** from line 32 to line 76. If the user ID used to log in starts with an m, the manager toolbar is shown, with multiple dropdowns. The dropdowns include Personal (book, bookings, and history), Timesheets (booking chart and history), and Employees (register and manage). The employee toolbar is much simpler, with just the basic functions of booking and viewing.

#### b. <ins> /, /change, /register, and /logout</ins>
#####
These routes are responsible for accessibility to Toolie via user's accounts.

It starts with registering an account. In **_register.html_**, the instructions on how to register are clearly stated for easy registering by the manager. When the manager registers a user, in the /register route, the data is saved in the users database with a default password, "Password". 

The page **_change.html_** allows for a user to change their password. It is simple, only requiring the user's ID, new password, and a confirmation of the new password. The error checking is done via the route /change. It ensures that firstly, the user exists, then if the user does exist, the new password is hashed before being saved into the users database.

The page **_login.html_** is the login page and also the default route when the user opens the website. This makes it convenient for the user to quickly access the tool booking system. The route /, ensures that the user ID and password entered are registered and correct before allowing the user to access the system. Additionally, this is where the differentiation of manager and employee happens. If the user ID starts with an e, it redirects to /employeehome and if it starts with an m, it redirects to /managerhome.

The /logout route just enables the user to logout. 

#### c. <ins>/employeelist and /remove</ins>
##### 
This route pulls all the data from the users table and displays it on the **_employeelist.html_** page in a table. The table is simple with only the employee name and user ID. Beside each employee, there is a remove button and through the /remove route, it enables the manager to remove an old employee and all their bookings, if any. Furthermore, there is a search bar for the employer to search for any names, given that the list of employees increases.

#### d. <ins>/book, /bookings, and /allbookings</ins>
#####
These routes are responsible for the actual booking system of TooliE. In **_book.html_**, the booking form has three fields. The tool, the date, and the timeslot. The user does not have to enter their user ID as in /book, the user ID is pulled from the session. The dates are restricted to only up to 2 weeks in advance to prevent users from over booking. The dropdown in the dates and the timeslot enable easier selection. 

In the route /book, server side error detection is present to prevent the user from mis-booking and messing up the system. This can be seen under the comment #Ensuring the valyes are valid. 

In **_bookings.html_**, the user's personal bookings are shown in a table. Each row will show the tool booked, the date and time of booking and 2 options - either cancel the booking or mark the booking as completed. There is also the search bar.

In **_allbookings.html_**, all the bookings are shown for the manager as a timesheet. 

#### e. <ins>/completedbookings, /removebooking, /bookinghistory, and /bookinghistorymgr</ins>
#####
These routes will redirect the user to the tables showing the history. In **_bookinghistory.html_**, the table for a user's personal history in shown while in **_bookinghistorymgr.html_**, the history for the whole team is shown. The search bar is available for both pages

The route /completedbookings enables the user to mark their booking as completed. This route will delete the booking from the bookings database and add it to the history database with the status as 'Completed'. The route /removebooking does the same, but instead marks the status as being 'Deleted'. This way, the employee and manager will know which bookings are actually attended. 

## Design choices I debated 
#### 1. Having the register page accessed only by a manager
#####
Initially, register was in my toolbar, accessible even without logging in. However, this could cause non-employee or non-managers 'hijacking' the TooliE system. Having this page only accessed once a manager logs in ensures that only approved users are registered and can subsequently log in. 

#### 2. Flash messages instead of rendering apology pages
#####
In layout.html, lines 95 to 105 describe the flash function which shows flash messages for different actions. This ensures users know their if their actions have been successfully done or whether they have made errors. This is done in replacement of rendering an apology page as it keeps the user on the same page, making the user experience smoother. The user will be able to see their error until the error is fixed.

#### 3. Having only 2 week in advace booking 
#####
Initially, the user could access the whole calendar, allowing them to book a tool any day of any month of any year. However, this could cause issues in two places. Firstly, users could book tools on days that are already over, which clutters the bookings page with unnecessary bookings. Secondly, it makes it hard for the manager to track all bookings if there was a possibility of the booking being for next year, which would have been irrelevant for the time being. Hence, only having 2 week in advance booking enables the user to only book tools for the next 2 weeks only. This updates everyday.

#### 4. Having both quick access buttons and the toolbar
#####
This is especially important for the manager homepage. The most commonly used features by the managers would most likely be booking a tool, seeing the timesheet and registering a new employee. Hence these were chosen to be quick access buttons. This would make user experience faster as it is easier to click the buttons straight from the homepage, right after logging in, rather than having to drag the mouse to the toolbar, waiting for and searching for the correct dropdown to load and click. 
