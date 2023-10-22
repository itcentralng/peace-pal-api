from app import ma
from app.guardian.model import *

class GuardianSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Guardian
        exclude = ('is_deleted',)