from App.models import Review, Staff, Student
from App.database import db
from sqlalchemy.exc import IntegrityError


def create_review(staff_id, student_id, content):
    reviewer = Staff.query.filter_by(id=staff_id).first()
    if not reviewer:
        raise ValueError(f"Staff member with id '{staff_id}' does not exist.")

    reviewee = Student.query.filter_by(id=student_id).first()
    if not reviewee:
        raise ValueError(f"Student with id '{student_id}' does not exist.")

    try:
        new_review = Review(staff_id, student_id, content)
        db.session.add(new_review)
        db.session.commit()
        return new_review
    except IntegrityError as e:
        db.session.rollback()
        raise e


def get_review(id):
    return Review.query.get(id)


def get_reviews_by_staff_id(staff_id):
    return Review.query.filter_by(staff_id=staff_id).all()


def get_reviews_by_student_id(student_id):
    return Review.query.filter_by(student_id=student_id).all()


def get_all_reviews():
    return Review.query.all()


def get_all_reviews_json():
    reviews = Review.query.all()
    if not reviews:
        return []
    reviews = [review.get_json() for review in reviews]
    return reviews


def update_review(id, staff_id, student_id, content):
    review = get_review(id)
    if review:
        review.staff_id = staff_id
        review.student_id = student_id
        review.content = content
        
        try:
            db.session.commit()
            return review
        except IntegrityError as e:
            db.session.rollback()
            raise e
    return None