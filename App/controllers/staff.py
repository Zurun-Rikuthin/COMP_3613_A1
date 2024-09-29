from App.models import Staff
from App.database import db


def create_staff(username, password, is_admin=False):
    newStaff = Staff(username=username, password=password, is_admin=is_admin)
    db.session.add(newStaff)
    db.session.commit()
    return newStaff
