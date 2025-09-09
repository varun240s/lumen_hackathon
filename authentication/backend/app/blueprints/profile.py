from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import User

profile_ns = Namespace('profile', description='Profile operations')

@profile_ns.route('/')
class UserProfile(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if user:
            return {'username': user.username}, 200
        return {'message': 'User not found'}, 404
