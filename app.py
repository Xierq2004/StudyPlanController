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


@app.route("/subjects/<int:subject_id>/edit", methods=["GET", "POST"])
def edit_subject(subject_id):
    subject = Subject.query.get_or_404(subject_id)

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        code = request.form.get("code", "").strip().upper()
        colour = request.form.get("colour", "#2563eb")

        if not name or not code:
            flash("Subject name and code are required.", "error")
            return render_template(
                "edit_subject.html",
               subjects=all_subjects
            )

        duplicate_subject = Subject.query.filter(
            Subject.code == code,
            Subject.id != subject.id
        ).first()

        if duplicate_subject:
            flash("This subject code already exists.", "error")
            return render_template(
                "edit_subject.html",
                subjects=all_subjects
            )

        subject.name = name
        subject.code = code
        subject.colour = colour

        db.session.commit()

        flash("Subject updated successfully.", "success")
        return redirect(url_for("subjects"))

    return render_template(
        "edit_subject.html",
        subjects=all_subjects
    )


@app.route("/subjects/<int:subject_id>/delete", methods=["POST"])
def delete_subject(subject_id):
    subject = Subject.query.get_or_404(subject_id)

    db.session.delete(subject)
    db.session.commit()

    flash("Subject deleted successfully.", "success")
    return redirect(url_for("subjects"))


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)