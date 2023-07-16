from flask_app import app
from flask import request ,render_template, session, redirect, flash
from flask_app.models.review import Review
from flask_app.models.sitter import Sitter
from flask_app.models import user
from flask_app.controllers import users

@app.route("/review/<int:sitter_id>/create", methods=['POST'])
def create_review(sitter_id):
    data ={ 
            **request.form,
            'user_id':session['user_id'],
            'sitter_id':sitter_id
        }
    print(data)
    aaa = Review.create(data)
    print(aaa)
    return redirect('/users/'+str(sitter_id)+'/sitterprofile')