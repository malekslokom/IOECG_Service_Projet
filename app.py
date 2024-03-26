from flask import Flask, jsonify,request
from flask_cors import CORS
import json
from consul import register_service_with_consul,SERVICE_PORT
from datetime import datetime
from database import db,Projets

app = Flask(__name__)
CORS(app)

#connexion bdd
app.config["SQLALCHEMY_DATABASE_URI"]= 'postgresql://postgres:postgresql@localhost:5432/IOECG'  #Windows
#app.config["SQLALCHEMY_DATABASE_URI"]= 'postgresql://postgres:postgresql@localhost:5433/IOECG' #Mac
db.init_app(app)   #Lie l'aplication à la base de donnée


@app.route('/api/projets/health')
def health():
    return jsonify({"status": "up"})

@app.route('/api/projets/',methods=["GET"])
def getAll():
    projets = Projets.query.all()  # Récupère tous les projets de la base de données
    projets_data = [{'idproject': projet.id_project,    #Il faut mettre le nom des attributs de l'object 'Projet' (interface Projet)
                     'nom': projet.name_project,
                     'version': projet.description_project,
                     'dateCreation': projet.created_at.strftime('%d-%m-%Y'),
                     'auteur': projet.created_by,
                     'type': projet.type_project.value} for projet in projets]
    return jsonify(projets_data)

# def getAll():
#     with open('projectSaticData.json') as f: 
#         data = json.load(f)
#     return jsonify(data) 


@app.route('/api/projets/<int:id>',methods=["GET"])
def getProjetById(id):
    print(id)

    projet = Projets.query.filter_by(id_project=id).first()  # Récupère le projet 
    if projet:
        projet_json = {
            'id': projet.id_project,
            'dateCreation': projet.created_at.strftime('%d-%m-%Y'),
            'last_updated_at': projet.last_updated_at,
            'nom': projet.name_project,
            'version': projet.description_project,
            'auteur': projet.created_by,
            'type': projet.type_project.value  #  accédez à la valeur avec .value
        }
        return jsonify(projet_json)
    else:
        return jsonify({"error": "Project not found"}), 404
    
    # with open('projectSaticData.json') as f: 
    #     projects = json.load(f)
    #     project=[item for item in projects if item["id"] ==id]
    #     print(project)
    # if project:
    #     return jsonify(project[0])
    # else:
    #     return jsonify({"error": "Project not found"}), 404 



@app.route('/api/projets/',methods=["POST"])
def createProjet():
    data = request.json  #dans get(), on met les clés du formulaire
    name = data.get('Nom')
    created_at = data.get('dateCreation')
    description = data.get('Version')
    created_by = data.get('auteur')    #pour le moment, il y a un nom par défaut (voir database.py)
    type_project = data.get('Type')

    if not all([name, type_project]):
        return jsonify({"error": "Veuillez fournir toutes les données requises"}), 400
    
    # Création du nouveau Projet
    new_project = Projets(name_project=name, created_at=created_at, description_project=description, created_by=created_by,
                              type_project=type_project)   

    # Ajouter dans la bdd
    db.session.add(new_project)
    try:
        # Valider et enregistrer les modifications dans la bdd
        db.session.commit()
        return jsonify({"message": "Projet créé avec succès"}), 201
    except Exception as e:
        # Erreur, annuler les modifications et renvoyer un message d'erreur
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


def convert_date(date_str):
    """Converts a date string from DD-MM-YYYY to a datetime object."""
    return datetime.strptime(date_str, "%d-%m-%Y")


@app.route('/api/projets/filter', methods=['GET'])
def filter_data():
    start_date_str = request.args.get('start_date', '')
    end_date_str = request.args.get('end_date', '')
    search_term = request.args.get('search_term', '').lower()
    # Convert the start and end dates from DD-MM-YYYY to datetime objects
    start_date = convert_date(start_date_str) if start_date_str else None
    end_date = convert_date(end_date_str) if end_date_str else None

    with open('projectSaticData.json') as f:
        data = json.load(f)
        filtered_data = []
        for item in data:
            item_date = convert_date(item['dateCreation'])
            if ((not start_date or item_date >= start_date) and
                (not end_date or item_date <= end_date) and
                (not search_term or search_term in item['nom'].lower() or search_term in item['type'].lower())):
                filtered_data.append(item)

        if filtered_data:
            return jsonify(filtered_data)
        else:
            return jsonify({"error": "No projects found matching the criteria"}), 404
        


@app.route('/api/projets/<int:id>',methods=["DELETE"])
def deleteProjetById(id):
    print(id)
    projet = Projets.query.filter_by(id_project=id).first()  # Récupère le projet 
    if projet:
        db.session.delete(projet)
        db.session.commit()
        return jsonify({"message": "Projet supprimé avec succès"}), 201
    else: 
        return jsonify({"error": "Project not found"}), 404


if __name__ == "__main__":
    register_service_with_consul()
    app.run(debug=True, port=SERVICE_PORT, host='0.0.0.0')  # Utilisez '0.0.0.0' pour rendre votre service accessible à partir d'autres machines sur le réseau
