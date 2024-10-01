import click
import pytest
import sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup
from sqlalchemy.exc import IntegrityError

from App.database import db, get_migrate
from App.models import Staff, Student, User, Review
from App.main import create_app
from App.controllers.initialize import initialize
from App.controllers.review import (create_review, get_review, get_reviews_by_staff_id,
                                    get_reviews_by_student_id, get_all_reviews, get_all_reviews_json, update_review)
from App.controllers.staff import (create_staff, get_staff, get_all_staff, get_all_staff_json, get_all_normal_staff,
                                   get_all_admin_staff, get_all_normal_staff_json, get_all_admin_staff_json, update_staff)
from App.controllers.student import (create_student, get_student, get_students_by_first_name,
                                     get_students_by_last_name, get_all_students, get_all_students_json, update_student)
from App.controllers.user import (
    create_user, get_user_by_username, get_user, get_all_users, get_all_users_json, update_user)

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database


@ app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database intialized')


'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands')

# Then define the command and any parameters and annotate it with the group (@)


@ user_cli.command("create", help="Creates a user")
@ click.argument("username", default="rob")
@ click.argument("password", default="robpass")
def create_user_command(username, password):
    try:
        create_user(username, password)
    except ValueError as e:
        print(f"Error: {e}")
    except IntegrityError as e:
        print(f"Database error: {e}")
    else:
        print(f'User {username} created!')

# this command will be : flask user create bob bobpass


@ user_cli.command("list", help="Lists users in the database")
@ click.option("--json", is_flag=True, help="Changes output format from a tuple string to JSON")
def list_user_command(json):
    if json:
        print(get_all_users_json())
    else:
        print(get_all_users())


app.cli.add_command(user_cli)  # add the group to the cli


'''
Staff Commands
'''

staff_cli = AppGroup("staff", help="Staff object command")


@ staff_cli.command("create", help="Creates a staff-type user")
@ click.argument("username", default="helpie")
@ click.argument("password", default="helpiepass")
@ click.option("--is-admin", is_flag=True, help="Grants the user admin-level privilidges")
def create_staff_command(username, password, is_admin):
    try:
        create_staff(username, password, is_admin)
    except ValueError as e:
        print(f"Error: {e}")
    except IntegrityError as e:
        print(f"Database error: {e}")
    else:
        print(f'Staff member {username} created!')


@ staff_cli.command("list", help="Lists staff members in the database")
@ click.option("--json", is_flag=True, help="Changes output format from a tuple string to JSON")
def list_staff_command(json):
    if json:
        print(get_all_staff_json())
    else:
        print(get_all_staff())


app.cli.add_command(staff_cli)

'''
Student Commands
'''

student_cli = AppGroup("student", help="Student object command")


@ student_cli.command("create", help="Creates a student data object")
@ click.argument("firstname", default="Jane")
@ click.argument("lastname", default="Doe")
def create_staff_command(firstname, lastname):
    try:
        create_student(firstname, lastname)
    except ValueError as e:
        print(f"Error: {e}")
    except IntegrityError as e:
        print(f"Database error: {e}")
    else:
        print(f'Student {firstname} {lastname} created!')


@ student_cli.command("list", help="Lists students in the database")
@ click.option("--json", is_flag=True, help="Changes output format from a tuple string to JSON")
def list_student_command(json):
    if json:
        print(get_all_students_json())
    else:
        print(get_all_students())


app.cli.add_command(student_cli)

'''
Review Commands
'''

review_cli = AppGroup("review", help="Review object command")


@ review_cli.command("create", help="Creates a student review")
@ click.argument("staff_id")
@ click.argument("student_id")
@ click.argument("content", nargs=-1)
def create_review_command(staff_id, student_id, content):
    content_str = " ".join(content)

    try:
        create_review(staff_id, student_id, content_str)
    except ValueError as e:
        print(f"Error: {e}")
    except IntegrityError as e:
        print(f"Database error: {e}")
    else:
        print(
            f'Review by staff with id {staff_id} for student with id {student_id} created!')


@ review_cli.command("list", help="Lists reviews in the database")
@ click.option("--json", is_flag=True, help="Changes output format from a tuple string to JSON")
def list_review_command(json):
    if json:
        print(get_all_reviews_json())
    else:
        print(get_all_reviews())


app.cli.add_command(review_cli)


'''
Test Commands
'''

test = AppGroup('test', help='Testing commands')


@ test.command("user", help="Run User tests")
@ click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))


app.cli.add_command(test)
