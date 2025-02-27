from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import User, db, Contact, contact_schema, contacts_schema

api = Blueprint('api', __name__, url_prefix='/api')
site = Blueprint('site',__name__, template_folder='site_templates')

@api.route('/getdata')
def getdata():
    return {'some': 'value'}

@api.route('/contacts', methods = ['POST'])
@token_required
def create_contact(current_user_token):
    name = request.json['name']
    email = request.json['email']
    phone_number = request.json['phone_number']
    address = request.json['address']
    user_token = current_user_token.token

    print(f'Big tester: {current_user_token.token}')

    contact = Contact(name, email, phone_number, address, user_token = user_token)

    db.session.add(contact)
    db.session.commit()

    response = contact_schema.dump(contact)
    return jsonify(response)

@api.route('/contacts', methods = ['GET'])
@token_required
def get_usercontact(current_user_token):
    a_user = current_user_token.token
    contacts = Contact.query.filter_by(user_token = a_user).all()
    response = contacts_schema.dump(contacts)
    return jsonify(response)

@api.route('/contacts/<id>', methods = ['GET'])
@token_required
def get_contact_two(current_user_token, id):
    fan = current_user_token.token
    if fan == current_user_token.token:
        contact = Contact.query.get(id)
        response = contact_schema.dump(contact)
        return jsonify(response)
    else:
        return jsonify({"message": "Valid Token Required"}),401

@api.route('/contacts/<id>', methods = ['POST','PUT'])
@token_required
def update_contact(current_user_token,id):
    contact = Contact.query.get(id) 
    contact.name = request.json['name']
    contact.email = request.json['email']
    contact.phone_number = request.json['phone_number']
    contact.address = request.json['address']
    contact.user_token = current_user_token.token

    db.session.commit()
    response = contacts_schema.dump(contact)
    return jsonify(response)


# DELETE car ENDPOINT
@api.route('/contacts/<id>', methods = ['DELETE'])
@token_required
def delete_contact(current_user_token, id):
    contact = Contact.query.get(id)
    db.session.delete(contact)
    db.session.commit()
    response = contact_schema.dump(contact)
    return jsonify(response)

@site.route('/')
def home():
    return render_template('index.html')

@site.route('/profile')
def profile():
    return render_template('profile.html')