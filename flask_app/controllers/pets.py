from flask_app import app
from flask import request ,render_template, session, redirect, flash
from flask_app.models import pet
import os
from werkzeug.utils import secure_filename
UPLOAD_FOLDER='flask_app/static/uploads/'
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
#app.config['MAX_CONTENT_LENGTH']=16*1024*1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS



# SHOW PROFILE USER WITH PETS


@app.route('/users/profile')
def show_profile():
    data = {
        'user_id' : session['user_id']
    }
    pets = pet.Pet.show_user_pets(data)
    
    
    return render_template('userprofile.html',pets = pets)

#   SHOW FORM TO ADD PET

@app.route('/users/pet/show')
def show_add_pet():
    return render_template('petcreation.html')

#  CREATE A PET IN THE DB

@app.route('/users/pet/create', methods=['POST'])
def add_pet():
    data = {
        **request.form,
        'image':request.files['file'].filename,
        "user_id" : session['user_id']
    }
    pet_id = pet.Pet.create_pet(data)
    session['pet_id'] = pet_id
    file = request.files['file']
    print(file.filename)
    session['image_pet']= '/static/uploads/'+file.filename
    print(session['image'],"gggggggggggggggggggggggggggggggggggggg")
    if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print(filename,'eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee')
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('Image successfully uploaded and displayed below')
            return redirect('/users/profile')

# SHOW PET INFORMATION
@app.route('/users/<int:pet_id>/show')
def one_pet_info(pet_id):
    data = {
        'id' : pet_id
    }
    print(data)
    session['image_pet']='/static/uploads/'+pet.Pet.get_image({'id':pet_id})
    one_pet = pet.Pet.show_one_pet(data)
    return render_template('showpet.html',one_pet = one_pet)

# SHOW FORM TO EDIT PET

@app.route('/users/<int:pet_id>/edit')
def edit_pet_form(pet_id):
    data = {
        'id' : pet_id
    }
    one_pet = pet.Pet.show_one_pet(data)
    return render_template('petedit.html',one_pet=one_pet)

# EDIT A PET

@app.route('/users/<int:pet_id>/update', methods=['POST'])
def edit_pet(pet_id):
    data = {
        **request.form,
        'id' : pet_id
    }
    pet.Pet.update_pet(data)
    return redirect('/users/profile')

#  DELETE PET 

@app.route('/users/<int:pet_id>/destroy')
def remove_pet(pet_id):
    data = {
        "id" : pet_id
    }
    pet.Pet.delete_pet(data)
    return redirect('/users/profile')