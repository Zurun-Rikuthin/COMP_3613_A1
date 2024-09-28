from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    # Discriminator for polymorphism
    type = db.Column(db.String(20), nullable=False)

    # https://docs.sqlalchemy.org/en/20/orm/inheritance.html#single-inheritance
    __mapper_args__ = {
        'polymorphic_on': "type",
        'polymorphic_identity': "user"
    }

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def get_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'type': self.type
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)
