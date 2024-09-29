from App.database import db
from .user import User


class Staff(User):
    # No __tablename__ here in single table inheritance (STI); we inherit from the base table (i.e., User)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    reviews = db.relationship(
        "Review", back_populates="writer", lazy=True, cascade="all, delete-orphan")

    # https://docs.sqlalchemy.org/en/20/orm/inheritance.html#single-inheritance
    __mapper_args__ = {
        "polymorphic_identity": "staff"
    }

    def __init__(self, username, password, is_admin=False):
        super().__init__(username, password)
        self.is_admin = is_admin

    def get_json(self):
        data = super().get_json()
        data.update({
            "type": "admin" if self.is_admin else "staff",
            "is_admin": self.is_admin})

        return data
