# Blueprint : make this file act as blueprint of the application and has many route
# inside it rather than make all the app routes inside one files.
from flask import Blueprint, render_template, request, jsonify, redirect, Response, make_response
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
        note = request.form.get('notedata')
        # validate the note
        if note=="":
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
@login_required
def deletenote():
    # grap the data body from the request
    # data come with the request as body attribute {} in json format
    dataWithRequest = request.data
    note = json.loads(dataWithRequest)  # convert json {} to python dict {}
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        # this note obj represent the note row in the db with the specific id, so you can grap the other
        # data with this record from obj.fieldname
        # make assure that note user owner is the one who going to delete it
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            # this flash will be shown in the first rendering page
            flash('Note is deleted successfully', category='success')
            return json.dumps({"status": "Note issssss deleted successfully"}), {"Content-Type": "application/json"}
            return jsonify({'status': 'Note is deleted successfully'})
        else:
            return jsonify({'status': "Note Owner is not the person who delete it"})
    else:
        return jsonify({'status': "Note is not founded on the DB"})


# handle the form delete request and delete the note with its id
@views.route('delete-note-2', methods=['post'])
@login_required
def deletenote2():
    # grap the data body from the request
    # data come with the request as body attribute {} in json format
    # if the data is sent with post request 
    noteid = request.form.get('noteid')
    print(f"note id is {noteid}")
    # if the data is sent with get request 
    # noteid = request.args.get('noteid') 
    # print(f"note id is {noteid}")
    note = Note.query.get(noteid)
    if note:
        # this note obj represent the note row in the db with the specific id, so you can grap the other
        # data with this record from obj.fieldname
        # make assure that note user owner is the one who going to delete it
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            # this flash will be shown in the first rendering page
            flash('Note is deleted successfully', category='success')
            return redirect('/')
        else:
            flash("Note Owner is not the person who delete it")
            return redirect('/')
    else:
        flash("Note is not founded on the DB")
        return redirect('/')


@views.route('update-note',methods=['post','get'])
@login_required
def update():
    # display the update html page
    if request.method=="GET" :
        noteid = request.args.get('noteid')
        note = db.session.query(Note).get(noteid)
        # note = Note.query.get(noteid)
        if note is None:
            flash('Note is not existed in DB ! ', category='error')
            return redirect('/')
        elif note.user_id != current_user.id:
            flash('You are not authorized to update this note',category='error')
            return redirect('/')
        else:
            return render_template('updateNote.html', user=current_user, note=note)
    elif request.method=="POST":
        noteid = request.form.get('noteid')
        notedata = request.form.get('notedata')
        note = Note.query.get(noteid)
        if note.user_id != current_user.id:
            flash('You are not authorized to update this note',category='error')
            return redirect('/')
        elif notedata == "":
            flash(f'{current_user.first_name} you cannot update your message with empty text !',category='error')
            return redirect('/')
        else:
            # update the content of note
            note.data = notedata
            db.session.add(note)
            db.session.commit()        
            flash('Note is updated successfully', category='success')
            return redirect('/')
