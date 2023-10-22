from flask import Blueprint, g, request
from app.route_guard import auth_required

from app.patient.model import *
from app.patient.schema import *
from app.user.model import User

bp = Blueprint('patient', __name__)

@bp.post('/patient')
@auth_required('guardian')
def create_patient():
    name = request.json.get('name')
    email = request.json.get('email')
    phone = request.json.get('phone')
    password = request.json.get('password', 'password')
    guardian_id = g.user.id
    user = User.create(email, password, 'patient')
    patient = Patient.create(name, phone, guardian_id, user.id)
    return PatientSchema().dump(patient), 201

@bp.get('/patient/<int:id>')
@auth_required('guardian')
def get_patient(id):
    patient = Patient.get_by_id(id)
    if patient is None:
        return {'message': 'Patient not found'}, 404
    return PatientSchema().dump(patient), 200

@bp.patch('/patient/<int:id>')
@auth_required('guardian')
def update_patient(id):
    patient = Patient.get_by_id(id)
    if patient is None:
        return {'message': 'Patient not found'}, 404
    name = request.json.get('name')
    phone = request.json.get('phone')
    patient.update(name, phone)
    return PatientSchema().dump(patient), 200

@bp.delete('/patient/<int:id>')
@auth_required('guardian')
def delete_patient(id):
    patient = Patient.get_by_id(id)
    if patient is None:
        return {'message': 'Patient not found'}, 404
    user = User.get_by_id(patient.user_id)
    patient.delete()
    user.delete()
    return {'message': 'Patient deleted successfully'}, 200

@bp.get('/patients')
@auth_required('guardian')
def get_patients():
    patients = Patient.get_by_guardian_id(g.user.id)
    return PatientSchema(many=True).dump(patients), 200