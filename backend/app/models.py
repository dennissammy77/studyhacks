from datetime import datetime
from sqlalchemy.orm import validates
import re
from backend.app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)


    @validates('username')
    def validate_username(self, key, value):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise ValueError("Username must be a valid email address")
        return value

class Query(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    query_text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
