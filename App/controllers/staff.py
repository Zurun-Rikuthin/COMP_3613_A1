from App.models import Staff
from App.database import db
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError


def create_staff(username, password, is_admin=False):
    new_staff = Staff(username=username, password=password, is_admin=is_admin)
    db.session.add(new_staff)
    db.session.commit()
    return new_staff


def get_staff(id):
    return Staff.query.filter(Staff.id == id, or_(Staff.type == "staff", Staff.type == "admin")).first()


def get_all_normal_staff(id):
    return Staff.query.filter_by(id=id, type="staff").all()


def get_all_admin_staff(id):
    return Staff.query.filter_by(id=id, type="admin").all()


def get_all_normal_staff_json():
    staff_members = get_all_normal_staff()
    if not staff_members:
        return []
    staff_members = [staff_member.get_json() for staff_member in staff_members]
    return staff_members


def get_all_admin_staff_json():
    staff_members = get_all_admin_staff()
    if not staff_members:
        return []
    staff_members = [staff_member.get_json() for staff_member in staff_members]
    return staff_members


def update_staff(id, username, is_admin):
    staff = get_staff(id)
    if staff:
        staff.username = username
        staff.is_admin = is_admin

        try:
            db.session.commit()
            return staff
        except IntegrityError as e:
            db.session.rollback()
            raise e
    return None
