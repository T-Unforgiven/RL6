from flask import Blueprint, render_template, request, flash, jsonify, send_file
from flask_login import login_required, current_user
from .models import Note, Upload
from . import db
import json
from io import BytesIO

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)  
            db.session.add(new_note) 
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/manuals', methods=['GET'])
def manuals():
    return render_template("manuals.html", user=current_user)


@views.route('/manuals/upload', methods=['GET', 'POST'])
def upload():
	if request.method == 'POST':
		file = request.files['file']
		upload = Upload(filename=file.filename, data=file.read())
		db.session.add(upload)
		db.session.commit()
		return f'Uploaded: {file.filename}'
	return render_template('manuals.html')


@views.route('/manuals/download/<upload_id>')
def download(upload_id):
	upload = Upload.query.filter_by(id=upload_id).first()
	return send_file(BytesIO(upload.data), download_name=upload.filename, as_attachment=True )

