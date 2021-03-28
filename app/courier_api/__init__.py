import logging

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

from .settings import load_postgres_settings

pg_settings = load_postgres_settings()


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://" \
                                        f"{pg_settings['POSTGRES_USER']}" \
                                        f":{pg_settings['POSTGRES_PASSWORD']}" \
                                        f"@postgres-12.6/courier_api"

# postgres-12.6
app.config['JSON_SORT_KEYS'] = False
db = SQLAlchemy()
db.init_app(app)

@app.errorhandler(404)
def page_not_found(e):
    logging.warning('Resource not found')
    return jsonify(error='Resource not found'), 404

@app.errorhandler(405)
def wrong_method(e):
    logging.warning('Wrong method')
    return jsonify(error='Wrong method'), 405

@app.errorhandler(500)
def wrong_method(e):
    logging.error('Internal error')
    return jsonify(error='Internal error'), 500

from courier_api import server

with app.app_context():
    db.create_all()
