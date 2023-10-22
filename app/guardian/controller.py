from flask import Blueprint, request
from app.route_guard import auth_required

from app.guardian.model import *
from app.guardian.schema import *
from app.user.model import User

bp = Blueprint('guardian', __name__)

@bp.post('/guardian')
# @auth_required()
def create_guardian():
    name = request.json.get('name')
    phone = request.json.get('phone')
    email = request.json.get('email')
    password = request.json.get('password', 'password')
    user = User.create(email, password, 'guardian')
    guardian = Guardian.create(name, phone, user.id)
    return GuardianSchema().dump(guardian), 201

@bp.get('/guardian/<int:id>')
@auth_required('guardian', 'admin')
def get_guardian(id):
    guardian = Guardian.get_by_id(id)
    if guardian is None:
        return {'message': 'Guardian not found'}, 404
    return GuardianSchema().dump(guardian), 200

@bp.patch('/guardian/<int:id>')
@auth_required('guardian')
def update_guardian(id):
    guardian = Guardian.get_by_id(id)
    if guardian is None:
        return {'message': 'Guardian not found'}, 404
    guardian.update()
    return GuardianSchema().dump(guardian), 200

@bp.delete('/guardian/<int:id>')
@auth_required('guardian', 'admin')
def delete_guardian(id):
    guardian = Guardian.get_by_id(id)
    if guardian is None:
        return {'message': 'Guardian not found'}, 404
    guardian.delete()
    return {'message': 'Guardian deleted successfully'}, 200

@bp.get('/guardians')
@auth_required('admin')
def get_guardians():
    guardians = Guardian.get_all()
    return GuardianSchema(many=True).dump(guardians), 200