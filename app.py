from flask import Flask, jsonify
from flask_cors import CORS
import requests
import json
from consul import register_service_with_consul,SERVICE_PORT

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
if __name__ == "__main__":
    register_service_with_consul()
    app.run(debug=True, port=SERVICE_PORT, host='0.0.0.0')  # Utilisez '0.0.0.0' pour rendre votre service accessible à partir d'autres machines sur le réseau
