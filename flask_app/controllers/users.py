from flask_app import app
from flask import request ,render_template, session, redirect, flash
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
from flask_app.models.address import Address
from flask_app.models.pet import Pet
from flask_app.models.sitter import Sitter
from flask_app.models.review import Review
from flask_app.models.service import Service
import os
from werkzeug.utils import secure_filename
UPLOAD_FOLDER='flask_app/static/uploads/'
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
#app.config['MAX_CONTENT_LENGTH']=16*1024*1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS


bcrypt = Bcrypt(app)     # we are creating an object called bcrypt, 
                        # which is made by invoking the function Bcrypt with our app as an argument
@app.route('/')
def index():
    return render_template("landing.html")


@app.route('/login')
def login_page():
    return render_template("login.html")

@app.route('/register')
def register():
    return render_template('register.html')

#   CREATE A USER WITH ADDRESS

@app.route('/users/create',methods=['POST'])
def create_user():
    
    if(User.validate(request.form)):
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        data1 = {
            **request.form
        }
        address_id = Address.create_address(data1)
        print(request.files['file'].filename,'ssssssssssssssssssssssssssssssssssssssssssssss')
        data2 = {
            **request.form,
            'image':request.files['file'].filename,
            'password': pw_hash,
            'address_id' : address_id
        }
        user_id = User.create_user(data2)
        
        session['user_id'] = user_id
        file = request.files['file']
        print(file.filename)
        session['image']= '/static/uploads/'+file.filename
        print(session['image'],"gggggggggggggggggggggggggggggggggggggg")
        if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                print(filename,'eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee')
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                flash('Image successfully uploaded and displayed below')
                return redirect('/searching')
    return redirect('/register')

@app.route('/users/login', methods=['POST'])
def login():
    user_from_db = User.get_by_email({'email':request.form['email']})
    if(user_from_db):
        # check password
        if not bcrypt.check_password_hash(user_from_db.password, request.form['password']):
        # if we get False after checking the password
            flash("Invalid Password")
            return redirect('/')
        session['user_id'] = user_from_db.id
        session['image'] = '/static/uploads/'+User.get_image({'id':session['user_id']})
        print(session['image'],'rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr')
        return redirect('/searching')
    flash("Invalid Email")
    return redirect('/login')

# SEARCHING PAGE 

@app.route('/searching')
def show_search_page():
    # session['first_name'] = User.get_name({'id': session['user_id']})
    user_id = {'id' : session['user_id']}
    all_services = Service.retrive_service_in_users(user_id)
    print(all_services)
    first_name = User.get_name(user_id)
    session['first_name'] = first_name
    return render_template('searching.html',all_services = all_services)




# SEARCH FOR SITTERS FORM

@app.route('/users/sitter/search', methods=['POST'])
def search():
    user_id = session['user_id']
    state = request.form.get('state')
    city = request.form.get('city')
    is_boarding = request.form.get('is_boarding')
    is_house_sitting = request.form.get('is_house_sitting')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')

    session['search_data'] = {
        "user_id" : user_id,
        "state" : state,
        "city" : city,
        'is_boarding': is_boarding,
        'is_house_sitting': is_house_sitting,
        'start_date': start_date,
        'end_date': end_date,
    }
    return redirect('/dashboard')

# DISPLAY SITTERS IN DASHBOARD

@app.route('/dashboard')
def results():
    search_data = session.get('search_data')

    if search_data:
        all_sitters = User.get_sitters_by_search(search_data)
        # append the address to the all_sitters with the get_address_sitter
        is_boarding_value = int(session['search_data']['is_boarding'])
        is_house_value = int(session['search_data']['is_house_sitting'])
        return render_template('dashboard.html', all_sitters=all_sitters,is_boarding_value=is_boarding_value,is_house_value=is_house_value)
    else:
        # Handle case when no search data is found in the session
        return redirect('/searching')

# SHOW OTHER SITTER PROFILE 

@app.route('/users/<int:sitter_id>/sitterprofile')
def display_other_sitter_profile(sitter_id):
    data = {
        'user_id' : sitter_id
    }
    data2={
        'sitter_id':sitter_id
    }
    
    session['sitter_id'] = sitter_id
    one_user = User.get_one_user(data)
    one_sitter = Sitter.get_by_id(data)
    reviews = Review.get_sitter_review(data2)
    print(reviews)

    return render_template('sitterotherprofile.html',one_sitter=one_sitter,one_user=one_user,sitter_id=sitter_id,reviews=reviews)

#  DISPLAY CONTACT SITTER FORM
@app.route("/users/<int:sitter_id>/contactsitter")
def display_contact_form(sitter_id):
    data = {
        'user_id' : sitter_id
    }
    search_data = session['search_data']
    one_user = User.get_one_user(data)
    one_sitter = Sitter.get_by_id(data)
    all_pets = Pet.show_user_pets({'user_id':session['user_id']})
    return render_template('contactsitter.html',one_sitter=one_sitter,one_user=one_user,all_pets=all_pets,search_data=search_data)
    


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')