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

    def __repr__(self):
        return f"<Subject {self.code}>"