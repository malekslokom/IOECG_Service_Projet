import json
from datetime import datetime
from flask import jsonify, request
from models.datasets import db
from models.datasets import Analyses, AnalysesDatasets, Datasets, Projet
def health():
    return jsonify({"status": "up"})

def getAllProjects():
    projects = Projet.query.order_by(Projet.created_at.desc()).all()
    if projects:
        # Convertir les résultats en une liste de dictionnaires
        project_data=[{
            "id_project":project.id_project,
            "created_at":project.created_at,
            "name_project":project.name_project,
            "description_project":project.description_project,
            "created_by":project.created_by,
            "type_project":project.type_project
        
        } for project in projects]
        response = jsonify(project_data)
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return response 
    else:
        return jsonify({"error": "No projects found"}), 404
    
def getProjetById(id_project):
    project = Projet.query.filter_by(id_project=id_project).first()
    if project:
        project_data={
            "id_project":project.id_project,
            "created_at":project.created_at,
            "name_project":project.name_project,
            "description_project":project.description_project,
            "created_by":project.created_by,
            "type_project":project.type_project
        }
        print(project_data)
        return jsonify(project_data)
    else:
        return jsonify({"error": "Project not found"}), 404
def convert_date(date_str):
    """Converts a date string from DD-MM-YYYY to a datetime object."""
    return datetime.strptime(date_str, "%d-%m-%Y")

def getProjectsWithFilter():
    start_date_str = request.args.get('start_date', '')
    end_date_str = request.args.get('end_date', '')
    search_term = request.args.get('search_term', '').lower()
    # Convert the start and end dates from DD-MM-YYYY to datetime objects
    start_date = convert_date(start_date_str) if start_date_str else None
    end_date = convert_date(end_date_str) if end_date_str else None
 # Construction de la requête de filtrage basée sur les paramètres
    query = Projet.query
    if start_date:
        query = query.filter(Projet.created_at >= start_date)
    if end_date:
        query = query.filter(Projet.created_at <= end_date)
    if search_term:
        query = query.filter((Projet.name_project.ilike(f'%{search_term}%')) |
                             (Projet.description_project.ilike(f'%{search_term}%')) |
                             (Projet.created_by.ilike(f'%{search_term}%')) |
                             (Projet.type_project.ilike(f'%{search_term}%')) )

    # Exécution de la requête et récupération des résultats
    filtered_projects = query.all()

    if filtered_projects:
        # Convertir les résultats en une liste de dictionnaires
        project_data=[{
            "id_project":project.id_project,
            "created_at":project.created_at,
            "name_project":project.name_project,
            "description_project":project.description_project,
            "created_by":project.created_by,
            "type_project":project.type_project
        
        } for project in filtered_projects]
        return jsonify(project_data)
    else:
        return jsonify({"error": "No projects found matching the criteria"}), 404
    


def getDatasetsForProject(id_project):
    # Récupérer toutes les analyses pour ce projet
    analyses = Analyses.query.filter_by(id_project=id_project).all()

    # Initialiser une liste pour stocker les datasets avec leurs analyses
    datasets_info = []

    # Pour chaque analyse, récupérer les datasets associés
    for analyse in analyses:
        # Utiliser la table d'association pour trouver les datasets liés à l'analyse
        assoc_entries = db.session.query(AnalysesDatasets).filter_by(id_analysis=analyse.id_analysis).all()
        for entry in assoc_entries:
            # Vérifier si le dataset est déjà ajouté avec l'analyse actuelle
            existing_entry = next((item for item in datasets_info if item['id_dataset'] == entry.id_dataset and item['id_analysis'] == analyse.id_analysis), None)
            if not existing_entry:
                # Récupérer l'objet Datasets
                dataset = Datasets.query.filter_by(id_dataset=entry.id_dataset).first()
                if dataset:
                    datasets_info.append({
                        'id_dataset': dataset.id_dataset,
                        'created_at': dataset.created_at,
                        'name_dataset': dataset.name_dataset,
                        'description_dataset': dataset.description_dataset,
                        'type_dataset': dataset.type_dataset,
                        'leads_name': dataset.leads_name,
                        'study_name': dataset.study_name,
                        'study_details': dataset.study_details,
                        'source_name': dataset.source_name,
                        'source_details': dataset.source_details,
                        'id_analysis': analyse.id_analysis  # Ajouter l'ID de l'analyse
                    })

    # Convertir les datasets en format JSON et retourner
    return jsonify(datasets_info)

def getAnalysesForProject(id_project):
 # Récupérer toutes les analyses pour ce projet
    analyses = Analyses.query.filter_by(id_project=id_project).all()
    print("analyses projet")
    # Convertir les analyses en format JSON
    analyses_json = [{
        'id_analysis': analyse.id_analysis,
        'id_project':analyse.id_project,
        'created_at': analyse.created_at,
        'last_updated_at': analyse.last_updated_at,
        'name_analysis': analyse.name_analysis,
        'description_analysis': analyse.description_analysis,
        'created_by': analyse.created_by,

    } for analyse in analyses]

    return jsonify(analyses_json)
def createProjet():
    data = request.json  
    name_project = data.get('name_project')
    created_at = data.get('created_at')
    description = data.get('description_project')
    created_by = data.get('created_by')   
    type_project = data.get('type_project')
    if not all([name_project, type_project]):
        return jsonify({"error": "Veuillez fournir toutes les données requises"}), 400
    
    # Création du nouveau Projet
    new_project = Projet(name_project=name_project, created_at=created_at, description_project=description, created_by=created_by,
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

def deleteProjetById(id):
    print(id)
    projet = Projet.query.filter_by(id_project=id).first()  # Récupère le projet 
    if projet:
        db.session.delete(projet)
        db.session.commit()
        return jsonify({"message": "Projet supprimé avec succès"}), 201
    else: 
        return jsonify({"error": "Project not found"}), 404

def deleteDatasetsForProject(id_analysis,id_dataset):
    try:
        analysis_dataset = AnalysesDatasets.query \
            .filter_by(id_analysis=id_analysis, id_dataset=id_dataset) \
            .first()

        if not analysis_dataset:
            return jsonify({'error': 'Analysis dataset association not found'}), 404

        db.session.delete(analysis_dataset)
        db.session.commit()

        return jsonify({'message': 'Datasets deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
def convert_date(date_str):
    """Converts a date string from DD-MM-YYYY to a datetime object."""
    return datetime.strptime(date_str, "%d-%m-%Y")

def getDatasetsProjetctWithFilter(id_project):
    start_date_str = request.args.get('start_date', '')
    end_date_str = request.args.get('end_date', '')
    search_term = request.args.get('search_term', '').lower()

    start_date = convert_date(start_date_str) if start_date_str else None
    end_date = convert_date(end_date_str) if end_date_str else None

    query = db.session.query(
        Datasets.id_dataset,
        Datasets.created_at,
        Datasets.name_dataset,
        Datasets.description_dataset,
        Datasets.type_dataset,
        Datasets.leads_name,
        Datasets.study_name,
        Datasets.study_details,
        Datasets.source_name,
        Datasets.source_details,
        AnalysesDatasets.id_analysis
    ).join(AnalysesDatasets, AnalysesDatasets.id_dataset == Datasets.id_dataset)\
      .join(Analyses, Analyses.id_analysis == AnalysesDatasets.id_analysis)\
      .filter(Analyses.id_project == id_project)

    if start_date:
        query = query.filter(Datasets.created_at >= start_date)
    if end_date:
        query = query.filter(Datasets.created_at <= end_date)
    if search_term:
        query = query.filter((Datasets.name_dataset.ilike(f'%{search_term}%')) |
                             (Datasets.description_dataset.ilike(f'%{search_term}%')) |
                             (Datasets.type_dataset.ilike(f'%{search_term}%')) |
                             (Datasets.leads_name.ilike(f'%{search_term}%')) |
                             (Datasets.study_name.ilike(f'%{search_term}%')) |
                             (Datasets.study_details.ilike(f'%{search_term}%')) |
                             (Datasets.source_name.ilike(f'%{search_term}%')) |
                             (Datasets.source_details.ilike(f'%{search_term}%')))

    filtered_datasets = query.all()

    if filtered_datasets:
        dataset_data = [{
            "id_dataset": dataset.id_dataset,
            "created_at": dataset.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            "name_dataset": dataset.name_dataset,
            "description_dataset": dataset.description_dataset,
            "type_dataset": dataset.type_dataset,
            "leads_name": dataset.leads_name,
            "study_name": dataset.study_name,
            "study_details": dataset.study_details,
            "source_name": dataset.source_name,
            "source_details": dataset.source_details,
            "id_analysis": dataset.id_analysis  # Include the ID of the analysis
        } for dataset in filtered_datasets]
        return jsonify(dataset_data)
    else:
        return jsonify([])  # Return an empty list instead of an error