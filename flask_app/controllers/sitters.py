from flask_app import app
from flask import request ,render_template, session, redirect, flash
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
from flask_app.models.address import Address
from flask_app.models.pet import Pet
from flask_app.models.sitter import Sitter
from flask_app.models import user
from flask_app.controllers import users
from flask_app.models.service import Service

bcrypt = Bcrypt(app)     # we are creating an object called bcrypt, 
                        # which is made by invoking the function Bcrypt with our app as an argument


# SHOW SITTER FORM
@app.route('/sitter/new')
def new_sitter():
    data = {
        'user_id' : session['user_id']
    }
    one_address = Address.get_one_address_sitter(data)
    one_user = User.get_one_user(data)
    return render_template('new_sitter.html',one_address=one_address,one_user=one_user)

# CREATE SITTER IN DB

@app.route("/users/sitter/create", methods=['POST'])
def create_sitter():
    if(Sitter.validate(request.form)):
        data = { 
                **request.form,
                'user_id':session['user_id']
            }
        print(data)
        sitter_id = Sitter.create(data)
        session['sitter_id'] = sitter_id
        return redirect('/users/sitter/profile')
    return redirect('/sitter/new')

# SITTER PROFILE PAGE

@app.route('/users/sitter/profile')
def display_my_sitter_profile():
    data = {
        'user_id' : session['user_id']
    }
    one_user = User.get_one_user(data)
    one_sitter = Sitter.get_by_id(data)
    session['sitt_id'] = one_sitter.id
    print(session['sitt_id'])
    return render_template('sitterprofile.html',one_sitter=one_sitter,one_user=one_user)

# SHOW FORM EDIT SITTER

@app.route('/sitters/<int:user_id>/edit')
def edit_sitter(user_id):
    data = {
        'user_id' : user_id
    }
    one_address = Address.get_one_address_sitter(data)
    one_user = User.get_one_user(data)
    one_sitter = Sitter.get_one_sitter(data)
    return render_template('editsitterprofile.html',one_address=one_address,one_user=one_user,one_sitter=one_sitter)

# UPDATE SITTER PROFILE

@app.route('/sitters/<int:user_id>/edit', methods=['POST'])
def update_sitter(user_id):
    data = {
        **request.form,
        'user_id' : user_id
    }
    Sitter.update(data)
    
    return redirect('/users/sitter/profile')


#request
