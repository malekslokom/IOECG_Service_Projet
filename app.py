from flask import Flask, jsonify, request
from flask_cors import CORS
from config.config import Config
from consul import register_service_with_consul

from models.datasets import db
app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
db.init_app(app)


# les apis
from api import getDatasetsProjetctWithFilter, health, getAllProjects, getProjetById, getProjectsWithFilter,getAnalysesForProject,getDatasetsForProject,createProjet,deleteProjetById

# les routes
app.route('/api/projets/health')(health)
app.route('/api/projets/',methods=["GET"])(getAllProjects)
app.route('/api/projets/<int:id_project>',methods=["GET"])(getProjetById)
app.route('/api/projets/filter', methods=['GET'])(getProjectsWithFilter)
app.route('/api/projets/<int:id_project>/datasets')(getDatasetsForProject)
app.route('/api/projets/<int:id_project>/analyses')(getAnalysesForProject)
app.route('/api/projets/',methods=["POST"])(createProjet)
app.route('/api/projets/<int:id>',methods=["DELETE"])(deleteProjetById)
app.route('/api/projets/<int:id_project>/datasets/filter/',methods=["GET"])(getDatasetsProjetctWithFilter)
if __name__ == "__main__":
    register_service_with_consul()
    app.run(debug=True, port=Config.SERVICE_PORT)
