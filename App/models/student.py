from App.database import db


class Student(db.Model):
    __tablename__ = "student"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    reviews = db.relationship("Review", back_populates="reviewee", lazy=True)

    def get_json(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    def get_json(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name
        }
