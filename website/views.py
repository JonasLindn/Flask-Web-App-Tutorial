from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        note = request.form.get('note')#Gets the note from the HTML 

        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/new_project', methods=['GET', 'POST'])
@login_required
def new_project():
    return render_template("new_project.html", user=current_user)


@views.route('/project_info', methods=['GET', 'POST'])
@login_required
def project_info():
    return render_template("project_info.html", user=current_user)


@views.route('/rahmenbedingungen', methods=['GET', 'POST'])
@login_required
def rahmenbedingungen():
    return render_template("rahmenbedingungen.html", user=current_user)


@views.route('/priority', methods=['GET', 'POST'])
@login_required
def priority():
    return render_template("priority.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
