from flask_sqlalchemy import SQLAlchemy
from enum import Enum


db = SQLAlchemy()

class typeProject(Enum):
    Classification = 'Classification'
    Visualisation = 'Visualisation'
    Régression = 'Régression'

class Projets(db.Model):
    __tablename__='projets'

    id_project = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    last_updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    name_project = db.Column(db.String(255), nullable=False)
    description_project = db.Column(db.Text,default=None)
    created_by = db.Column(db.String(255), default= "Andy")
    type_project= db.Column(db.Enum(typeProject), nullable=None)