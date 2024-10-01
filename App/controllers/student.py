from App.models import Student
from App.database import db
from sqlalchemy.exc import IntegrityError


def create_student(first_name, last_name):
    new_student = Student(first_name, last_name)
    try:
        db.session.add(new_student)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        raise IntegrityError(e)
    else:
        return new_student


def get_student(id):
    return Student.query.get(id)


def get_students_by_first_name(first_name):
    return Student.query.filter_by(first_name=first_name).all()


def get_students_by_last_name(last_name):
    return Student.query.filter_by(first_name=last_name).all()


def get_all_students():
    return Student.query.all()


def get_all_students_json():
    students = Student.query.all()
    if not students:
        return []
    students = [student.get_json() for student in students]
    return students


def update_student(id, first_name, last_name):
    student = get_student(id)
    if student:
        student.first_name = first_name
        student.last_name = last_name

        try:
            db.session.commit()
            return student
        except IntegrityError as e:
            db.session.rollback()
            raise e
    return None
