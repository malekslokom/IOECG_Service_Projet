from flask_sqlalchemy import SQLAlchemy
from enum import Enum


db = SQLAlchemy()

class typeProject(Enum):
    Classification = 'Classification'
    Visualisation = 'Visualisation'
    Régression = 'Régression'

class Projets(db.Model):
    __tablename__ = 'projets'

    id_project = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now())
    last_updated_at = db.Column(db.TIMESTAMP, server_default=db.func.now(), onupdate=db.func.now())
    name_project = db.Column(db.String, nullable=False)
    description_project = db.Column(db.Text)
    created_by = db.Column(db.String, nullable=False)
    type_project = db.Column(db.String, nullable=False)

    __table_args__ = (
        db.CheckConstraint(type_project.in_(["Classification", "Régression", "Visualisation"]), name='check_type_project'),
    )
    # Define a one-to-many relationship with Analyses
    analyses = db.relationship('Analyses', backref='projet')

class Analyses(db.Model):
    __tablename__ = 'analyses'

    id_analysis = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_project = db.Column(db.Integer, db.ForeignKey('projets.id_project'))
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now())
    last_updated_at = db.Column(db.TIMESTAMP, server_default=db.func.now(), onupdate=db.func.now())
    name_analysis = db.Column(db.String, nullable=False)
    description_analysis = db.Column(db.Text)
    created_by = db.Column(db.String, nullable=False)
