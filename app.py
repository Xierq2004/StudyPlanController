from flask import Flask, flash, redirect, render_template, request, url_for
from config import Config
from models import Subject, db


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/subjects")
def subjects():
    all_subjects = Subject.query.order_by(Subject.code).all()
    return render_template(
        "subjects.html",
        subjects=all_subjects
    )


@app.route("/subjects/add", methods=["GET", "POST"])
def add_subject():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        code = request.form.get("code", "").strip().upper()
        colour = request.form.get("colour", "#2563eb")

        if not name or not code:
            flash("Subject name and code are required.", "error")
            return render_template("add_subject.html")

        existing_subject = Subject.query.filter_by(code=code).first()

        if existing_subject:
            flash("This subject code already exists.", "error")
            return render_template("add_subject.html")

        subject = Subject(
            name=name,
            code=code,
            colour=colour
        )

        db.session.add(subject)
        db.session.commit()

        flash("Subject added successfully.", "success")
        return redirect(url_for("subjects"))

    return render_template("add_subject.html")


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)