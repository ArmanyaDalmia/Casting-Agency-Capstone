import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from auth import AuthError, requires_auth
from models import *

def create_app(test_config=None):

  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)