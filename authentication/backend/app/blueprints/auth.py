from flask import request
from flask_restx import Namespace, Resource, fields
from ..models import User
from ..extensions import db, bcrypt
from flask_jwt_extended import create_access_token

auth_ns = Namespace('auth', description='Authentication operations')

# Model for the signup and login data
user_model = auth_ns.model('UserModel', {
    'username': fields.String(required=True, description='The username'),
    'password': fields.String(required=True, description='The password')
})

@auth_ns.route('/signup')
class Signup(Resource):
    @auth_ns.expect(user_model)
    def post(self):
        data = request.json
        username = data.get('username')
        password = data.get('password')

        if User.query.filter_by(username=username).first():
            return {'message': 'User already exists'}, 409

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return {'message': 'User created successfully'}, 201

@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(user_model)
    def post(self):
        data = request.json
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            access_token = create_access_token(identity=user.id)
            return {'access_token': access_token}, 200

        return {'message': 'Invalid credentials'}, 401
