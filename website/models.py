from matplotlib.style import available
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150))
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    user_type = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    middle_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    prefix = db.Column(db.String(150))
    file = db.Column(db.String(250))
    address = db.Column(db.String(150))
    age = db.Column(db.String(20))
    gender = db.Column(db.String(20))
    birthday = db.Column(db.String(50))
    phone_number = db.Column(db.String(20))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

class Company(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(250), unique=True)
    slots = db.Column(db.String(150))
    available_slot = db.Column(db.String(150))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

class Term(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    term_name = db.Column(db.String(250), unique=True)
    term_under = db.Column(db.String(250))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

class Trait(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    agr1 = db.Column(db.String(20))
    date = db.Column(db.String(20))
    time_started = db.Column(db.String(20))
    time_ended = db.Column(db.String(20))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))

class TraitFinal(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    agreeableness = db.Column(db.String(150))
    conscientiousness = db.Column(db.String(150))
    extroversion = db.Column(db.String(150))
    neuroticism = db.Column(db.String(150))
    openness = db.Column(db.String(150))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

class ResumeFinal(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    quality = db.Column(db.String(150))
    operations = db.Column(db.String(150))
    supplychain = db.Column(db.String(150))
    project = db.Column(db.String(150))
    data = db.Column(db.String(150))
    healthcare = db.Column(db.String(150))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())