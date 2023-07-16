from flask_app import app
from flask import request ,render_template, session, redirect, flash
from flask_app.models.service import Service

@app.route("/users/<int:sitter_id>/services", methods=['POST'])
def new_service(sitter_id):
    
    data = {
        **request.form,
        'sitter_id' : sitter_id
    }
    Service.create_service(data)
    return redirect('/dashboard')

# DISPLAY REQUEST TO THE SITTER

@app.route('/sitters/requests')
def show_requests():
    services = Service.retrive_service({'sitter_id':session['sitt_id']})
    print(services,'££'*55)
    print(session['sitt_id'],'$$'*555)
    return render_template('sitterpendingservices.html',services=services)

# EDIT REQUEST TO ACCEPTED

@app.route('/services/<int:service_id>/accept')
def update_requests_accepted(service_id):

    Service.update_accept({'id' : service_id})
    return redirect('/sitters/requests')

# EDIT REQUEST TO DECLINED


@app.route('/services/<int:service_id>/decline')
def update_request_declined(service_id):
    
    Service.update_decline({'id' : service_id})
    return redirect('/sitters/requests')

# SHOW REQUEST ACCEPTED
@app.route('/sitters/requests/accepted')
def show_request_accepted():
    services = Service.retrive_service({'sitter_id':session['sitt_id']})

    return render_template('sitteracceptedservices.html',services=services)

@app.route('/sitters/requests/declined')
def show_request_declined():
    services = Service.retrive_service({'sitter_id':session['sitt_id']})

    return render_template('sitterdeclinedservices.html',services=services)



