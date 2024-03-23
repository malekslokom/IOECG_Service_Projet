from flask import Flask, jsonify,request
from flask_cors import CORS
import json
from consul import register_service_with_consul,SERVICE_PORT
from datetime import datetime
app = Flask(__name__)
CORS(app)

@app.route('/api/projets/health')
def health():
    return jsonify({"status": "up"})

@app.route('/api/projets/',methods=["GET"])
def getAll():
    with open('projectSaticData.json') as f: 
        data = json.load(f)
    return jsonify(data)
@app.route('/api/projets/<int:id>',methods=["GET"])
def getProjetById(id):
    print(id)
    with open('projectSaticData.json') as f: 
        projects = json.load(f)
        project=[item for item in projects if item["id"] ==id]
        print(project)
    if project:
        return jsonify(project[0])
    else:
        return jsonify({"error": "Project not found"}), 404
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
if __name__ == "__main__":
    register_service_with_consul()
    app.run(debug=True, port=SERVICE_PORT, host='0.0.0.0')  # Utilisez '0.0.0.0' pour rendre votre service accessible à partir d'autres machines sur le réseau
