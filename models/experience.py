from sqlalchemy import CheckConstraint
from database import db  

class Experience(db.Model):
    __tablename__ = 'experiences'

    id_experience = db.Column(db.Integer, primary_key=True)
<<<<<<< HEAD
    name_experience = db.Column(db.String)
=======
>>>>>>> 989e07e7a150db3a99c2547e313029b06a56f57b
    models = db.Column(db.ARRAY(db.Integer), nullable=False)
    datasets = db.Column(db.ARRAY(db.Integer), nullable=False)
    nom_machine = db.Column(db.String())
    nb_gpu = db.Column(db.Integer)
    nb_processeurs = db.Column(db.Integer)
    heure_lancement = db.Column(db.Time, nullable=False, default= db.func.current_time())
    heure_fin_prevu = db.Column(db.Time)
    statut = db.Column(db.String(), nullable=False)
    resultat_prediction  = db.Column(db.ARRAY(db.Float))

    __table_args__ = (
        CheckConstraint(statut.in_(['En cours', 'Terminé']), name='check_statut'),
    )
