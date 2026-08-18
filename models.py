from datetime import datetime

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Subject(db.Model):
    __tablename__ = "subjects"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    colour = db.Column(
        db.String(20),
        nullable=False,
        default="#2563eb"
    )

    tasks = db.relationship(
        "StudyTask",
        backref="subject",
        lazy=True,
        cascade="all, delete-orphan"
    )


class StudyTask(db.Model):
    __tablename__ = "study_tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    due_date = db.Column(db.Date, nullable=False)
    priority = db.Column(
        db.String(20),
        nullable=False,
        default="Medium"
    )
    status = db.Column(
        db.String(20),
        nullable=False,
        default="Pending"
    )
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now
    )

    subject_id = db.Column(
        db.Integer,
        db.ForeignKey("subjects.id"),
        nullable=False
    )