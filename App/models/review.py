from App.database import db


class Review(db.Model):
    __tablename__ = "review"
    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.Integer, db.ForeignKey("staff.id"), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey(
        "student.id"), nullable=False)
    content = db.Column(db.String(4096), nullable=False)

    writer = db.relationship("Staff", back_populates="reviews", lazy=True)
    reviewee = db.relationship("Student", back_populates="reviews", lazy=True)

    def __init__(self, staff_id, student_id, content):
        self.staff_id = staff_id
        self.student_id = student_id
        self.content = content

    def get_json(self):
        return {
            "id": self.id,
            "staff_id": self.staff_id,
            "student_id": self.student_id,
            "content": self.content
        }
