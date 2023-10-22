from app import ma
from app.patient.model import *

class PatientSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Patient
        exclude = ('is_deleted',)