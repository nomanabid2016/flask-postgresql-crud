from flask import Flask, jsonify
from flask_cors import CORS
from app.task.controller import blueprint as task_blueprint
from config import Config
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = Config.DB.CONNECTION_STR
app.register_blueprint(task_blueprint)

db = SQLAlchemy(app)
cors = CORS(app, origins=["*"], resources={r"/*": {"origins": "*"}})




@app.errorhandler(Exception)
def handle_runtime_error(error):
    return jsonify({"error": str(error)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5006)
