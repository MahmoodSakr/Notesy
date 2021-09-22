# Blueprint : make this file act as blueprint of the application and has many route
# inside it rather than make all the app routes inside one files.
from flask import Blueprint, render_template, request, jsonify , Response , make_response
import json
from flask.helpers import flash
from flask_login import login_required, current_user
from . import db
from .models import Note
views = Blueprint('views', __name__)


@views.route('/', methods=['post', 'get'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        # validate the note
        if len(note) < 1:
            flash('Your note is empty ! ', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('You note has been added successfully', category='success')
    # for the get request to display the home page.html
    return render_template('home.html', user=current_user)

# handle the ajax request to delete the note once clicking on the button beside note


@views.route('delete-note', methods=['POST'])
def deletenote():
    # grap the data body from the request
    requestData = request.data  # data is the request body attribute {} in json format
    note = json.loads(requestData)  # convert json to python
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        # makre assure that its owner is goping to delete it
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            # this flash will be shown in the first rendering page
            flash('Note is deleted successfully',category='success')
            # return json.dumps({"status":"Note issssss deleted successfully"})
            return jsonify({'status': 'Note is deleted successfully'})
        else:
            return jsonify({'status': "Note Owner is not the person who delete it"})
    else:
        return jsonify({'status': "Note is not founded on the DB"})
