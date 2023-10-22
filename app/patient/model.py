from app import db

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    guardian_id = db.Column(db.Integer, db.ForeignKey("guardian.id"))
    name = db.Column(db.String)
    phone = db.Column(db.String, unique=True)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now())
    is_deleted = db.Column(db.Boolean, default=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, name=None, phone=None):
        self.name = name or self.name
        self.phone = phone or self.phone
        self.updated_at = db.func.now()
        db.session.commit()
    
    def delete(self):
        self.is_deleted = True
        self.updated_at = db.func.now()
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id, is_deleted=False).first()
    
    @classmethod
    def get_all(cls):
        return cls.query.filter_by(is_deleted=False).all()
    
    @classmethod
    def get_by_guardian_id(cls, guardian_id):
        return cls.query.filter_by(guardian_id=guardian_id).all()
    
    @classmethod
    def create(cls, name, phone, guardian_id, user_id=None):
        patient = cls(name=name, phone=phone, guardian_id=guardian_id, user_id=user_id)
        patient.save()
        return patient