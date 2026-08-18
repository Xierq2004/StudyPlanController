from datetime import datetime

from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    url_for
)

from config import Config
from models import StudyTask, Subject, db


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/subjects")
def subjects():
    all_subjects = Subject.query.order_by(
        Subject.code
    ).all()

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
            flash(
                "Subject name and code are required.",
                "error"
            )
            return render_template("add_subject.html")

        existing_subject = Subject.query.filter_by(
            code=code
        ).first()

        if existing_subject:
            flash(
                "This subject code already exists.",
                "error"
            )
            return render_template("add_subject.html")

        subject = Subject(
            name=name,
            code=code,
            colour=colour
        )

        db.session.add(subject)
        db.session.commit()

        flash(
            "Subject added successfully.",
            "success"
        )
        return redirect(url_for("subjects"))

    return render_template("add_subject.html")


@app.route(
    "/subjects/<int:subject_id>/edit",
    methods=["GET", "POST"]
)
def edit_subject(subject_id):
    subject = Subject.query.get_or_404(subject_id)

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        code = request.form.get("code", "").strip().upper()
        colour = request.form.get("colour", "#2563eb")

        if not name or not code:
            flash(
                "Subject name and code are required.",
                "error"
            )
            return render_template(
                "edit_subject.html",
                subject=subject
            )

        duplicate_subject = Subject.query.filter_by(
            code=code
        ).first()

        if (
            duplicate_subject
            and duplicate_subject.id != subject.id
        ):
            flash(
                "This subject code already exists.",
                "error"
            )
            return render_template(
                "edit_subject.html",
                subject=subject
            )

        subject.name = name
        subject.code = code
        subject.colour = colour

        db.session.commit()

        flash(
            "Subject updated successfully.",
            "success"
        )
        return redirect(url_for("subjects"))

    return render_template(
        "edit_subject.html",
        subject=subject
    )


@app.route(
    "/subjects/<int:subject_id>/delete",
    methods=["POST"]
)
def delete_subject(subject_id):
    subject = Subject.query.get_or_404(subject_id)

    db.session.delete(subject)
    db.session.commit()

    flash(
        "Subject deleted successfully.",
        "success"
    )
    return redirect(url_for("subjects"))


@app.route("/tasks")
def tasks():
    all_tasks = StudyTask.query.order_by(
        StudyTask.due_date
    ).all()

    return render_template(
        "tasks.html",
        tasks=all_tasks
    )


@app.route("/tasks/add", methods=["GET", "POST"])
def add_task():
    all_subjects = Subject.query.order_by(
        Subject.code
    ).all()

    if not all_subjects:
        flash(
            "Add a subject before creating a task.",
            "error"
        )
        return redirect(url_for("subjects"))

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get(
            "description",
            ""
        ).strip()
        due_date_text = request.form.get(
            "due_date",
            ""
        )
        priority = request.form.get(
            "priority",
            "Medium"
        )
        subject_id_text = request.form.get(
            "subject_id",
            ""
        )

        if not title or not due_date_text or not subject_id_text:
            flash(
                "Title, subject and due date are required.",
                "error"
            )
            return render_template(
                "add_task.html",
                subjects=all_subjects
            )

        try:
            due_date = datetime.strptime(
                due_date_text,
                "%Y-%m-%d"
            ).date()
        except ValueError:
            flash(
                "Enter a valid due date.",
                "error"
            )
            return render_template(
                "add_task.html",
                subjects=all_subjects
            )

        try:
            subject_id = int(subject_id_text)
        except ValueError:
            flash(
                "Select a valid subject.",
                "error"
            )
            return render_template(
                "add_task.html",
                subjects=all_subjects
            )

        subject = db.session.get(
            Subject,
            subject_id
        )

        if subject is None:
            flash(
                "The selected subject does not exist.",
                "error"
            )
            return render_template(
                "add_task.html",
                subjects=all_subjects
            )

        if priority not in {"Low", "Medium", "High"}:
            priority = "Medium"

        task = StudyTask(
            title=title,
            description=description,
            due_date=due_date,
            priority=priority,
            status="Pending",
            subject_id=subject.id
        )

        db.session.add(task)
        db.session.commit()

        flash(
            "Task added successfully.",
            "success"
        )
        return redirect(url_for("tasks"))

    return render_template(
        "add_task.html",
        subjects=all_subjects
    )


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )