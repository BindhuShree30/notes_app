from flask import (
    Blueprint,
    render_template,
    request,
    session,
    redirect,
    url_for,
    flash
)

from extensions import db
from models import Note


notes_bp = Blueprint(
    "notes",
    __name__
)


@notes_bp.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        flash(
            "You must be logged in to view this page",
            "warning"
        )
        return redirect(url_for("auth.login"))

    notes = Note.query.filter_by(
        user_id=session["user_id"]
    ).all()

    return render_template(
        "dashboard.html",
        notes=notes
    )


# Add Notes

@notes_bp.route("/add_note", methods=["GET", "POST"])
def add_note():

    if "user_id" not in session:
        flash(
            "You must be logged in to view this page",
            "warning"
        )
        return redirect(url_for("auth.login"))

    if request.method == "POST":

        title = request.form["title"]
        description = request.form["description"]

        note = Note(
            title=title,
            description=description,
            user_id=session["user_id"]
        )

        db.session.add(note)
        db.session.commit()

        flash(
            "Note added successfully",
            "success"
        )

        return redirect(
            url_for("notes.dashboard")
        )

    return render_template("add_note.html")


# Edit Notes

@notes_bp.route("/edit_note/<int:note_id>", methods=["GET", "POST"])
def edit_note(note_id):

    if "user_id" not in session:
        flash(
            "You must be logged in to view this page",
            "warning"
        )
        return redirect(url_for("auth.login"))

    note = Note.query.get_or_404(note_id)

    # Security check
    if note.user_id != session["user_id"]:
        flash(
            "You cannot edit this note",
            "danger"
        )
        return redirect(url_for("notes.dashboard"))

    if request.method == "POST":

        note.title = request.form["title"]
        note.description = request.form["description"]

        db.session.commit()

        flash(
            "Note updated successfully",
            "success"
        )

        return redirect(url_for("notes.dashboard"))

    return render_template(
        "edit_note.html",
        note=note
    )
#delete notes
    
@notes_bp.route("/delete_note/<int:note_id>", methods=["POST"])
def delete_note(note_id):

    if "user_id" not in session:
        flash(
            "You must be logged in to view this page",
            "warning"
        )
        return redirect(url_for("auth.login"))

    note = Note.query.get_or_404(note_id)

    # Security check
    if note.user_id != session["user_id"]:
        flash(
            "You cannot delete this note",
            "danger"
        )
        return redirect(url_for("notes.dashboard"))

    db.session.delete(note)
    db.session.commit()

    flash(
        "Note deleted successfully",
        "success"
    )

    return redirect(url_for("notes.dashboard"))
    
    