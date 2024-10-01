from App.models import User
from App.database import db
from sqlalchemy.exc import IntegrityError


def create_user(username, password):
    existing_user = get_user_by_username(username)
    if existing_user:
        raise ValueError(f"User with username '{username}' already exists.")

    try:
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return new_user
    except IntegrityError as e:
        db.session.rollback()
        raise e


def get_user_by_username(username):
    return User.query.filter_by(username=username).first()


def get_user(id):
    return User.query.get(id)


def get_all_users():
    return User.query.all()


def get_all_users_json():
    users = get_all_users()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users


def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username

        try:
            db.session.commit()
            return user
        except IntegrityError as e:
            db.session.rollback()
            raise e
    return None
