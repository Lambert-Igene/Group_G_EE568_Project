# Group G EE568 Project

- ER Diagram: ![er-diagram](https://user-images.githubusercontent.com/29764960/235255029-b3de6615-2ebb-4b29-8729-66435176ca41.png)
- Database Schema Diagram: ![database_model](https://user-images.githubusercontent.com/29764960/235255117-a00fd48d-c5b4-463c-aa28-72f842d5618e.png)
- Design Manual:
- User Manual:

## About

My team designed and implement a web-based university management system. The system made use of the university database that we have been working on since the beginning of this semester, but with some extension. The system utilizes Django web framework to connect to MySQL to hold together all components: loading data from the database, representing the data as Python objects, and dynamically creating a web page for displaying the data. The user interface was built using Django templates.

Our system provides the below functionalities and features to support three kinds of users: admins, profs, and students, as follows:
Admin can do the following: 
- F1. Roster: Create a list of professors sorted by one of the following criteria chosen by the admin: (1) by name (2) by dept, or (3) by salary. 
- F2. Salary: Create a table of min/max/average salaries by dept.
- F3. Performance: Given a professor's name, an academic year, and a semester, show the following for the professor: the total number of course sections taught during the semester, the total number of students taught, the total dollar amount of funding the professor has secured, and the total number of papers the professor has published.

Professors can do the following:
- F4. Create the list of course sections and the number of students enrolled in each section that the professor taught in a given semester
- F5. Create the list of students enrolled in a course section taught by the professor in a given semester

Students can do the following:
- F6. Query the list of course sections offered by dept in a given year and semester.

## Prerequisites
User needs to install the listed prerequisites before they can use this project:

- Python 3
- Django 
- MySQL Connector for Python


Installation
-----------------------------------------------
Clone this repository: 
```shell
git clone https://github.com/kanizfatima22/Group_G_EE568_Project/tree/master/Group_G_EE568_Project
```
Run the server:
```shell
python manage.py runserver
```
Open your browser and navigate to: http://127.0.0.1:8000


## Database Credentials
- MYSQL Username: group_g
- MYSQL Password: Group_G@EE568
- MYSQL Host: 128.153.13.175
- MYSQL Port: 3306
- MYSQL Database: university_group_g
- Terminal Command:
```shell
mysql -u group_g -h 128.153.13.175 -p
```


## Usage
The use the system, you can make use of the following user credentials:

### Admin
- Admin ID: `4321`
- Password: 12345`

### Professor
- Professor ID: `12345`
- Password: `12345`

### Student
- Student ID: `4321`
- Password: `12345`
