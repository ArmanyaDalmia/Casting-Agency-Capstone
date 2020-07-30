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

  # Use the after_request decorator to set Access-Control-Allow
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response
  


  # ===============================================================ROUTES===============================================================



  # =====================================GET Requests=====================================

  '''
  @ implement endpoint
    GET /actors
  '''
  @app.route('/actors')
  @requires_auth('get:actors')
  def get_actors(token):
    actors = Actor.query.order_by(Actor.id).all()

    try:
      return jsonify({
        'success': True,
        'actors': [actor.format() for actor in actors]
      })
    except:
      abort(404)


  '''
  @ implement endpoint
    GET /movies
  '''
  @app.route('/movies')
  @requires_auth('get:movies')
  def get_movies(token):

    movies = Movie.query.order_by(Movie.id).all()

    try:
      return jsonify({
        'success': True,
        'movies': [movie.format() for movie in movies]
      })
    except:
      abort(404)



  # =====================================POST Requests=====================================

  '''
  @ implement endpoint
    POST /actors
  '''
  @app.route('/actors', methods=['POST'])
  @requires_auth('post:actors')
  def create_actors(token):

    try:

      body = request.get_json()

      new_name = body.get('name', None)
      new_age = body.get('age', None)
      new_gender = body.get('gender', None)

      if new_name is None:
        abort(404)

      actor = Actor(name=new_name, age=new_age, gender=new_gender)
      actor.insert()

      return jsonify({
        'success': True,
        'actors': [actor.format()]
      })
    except:
      abort(422)


  '''
  @ implement endpoint
    POST /movies
  '''
  @app.route('/movies', methods=['POST'])
  @requires_auth('post:movies')
  def create_movies(token):

    try:

      body = request.get_json()

      new_title = body.get('title', None)
      new_release_date = body.get('release_date', None)

      if new_title is None:
        abort(404)

      movie = Movie(title=new_title, release_date=new_release_date)
      movie.insert()

      return jsonify({
        'success': True,
        'movies': [movie.format()]
      })
    except:
      abort(422)



  # =====================================PATCH Requests=====================================

  '''
  @ implement endpoint
    PATCH /actors/<id>
  '''
  @app.route('/actors/<id>', methods=['PATCH'])
  @requires_auth('patch:actors')
  def update_actors(token, id):

    actor = Actor.query.filter(Actor.id == id).one_or_none()
    if actor is None:
      abort(404)

    try:
      body = request.get_json()

      actor_name = body.get('name')
      actor_age = body.get('age')
      actor_gender = body.get('gender')

      if actor_name:
        actor.name = actor_name
      if actor_age:
        actor.age = actor_age
      if actor_gender:
        actor.gender = actor_gender

      actor.update()

      return jsonify({
        'success': True,
        'actors': [actor.format()]
      })

    except:
      abort(422)


  '''
  @ implement endpoint
    PATCH /movies/<id>
  '''
  @app.route('/movies/<id>', methods=['PATCH'])
  @requires_auth('patch:movies')
  def update_movies(token, id):

    movie = Movie.query.filter(Movie.id == id).one_or_none()
    if movie is None:
      abort(404)

    try:
      body = request.get_json()

      movie_title = body.get('title')
      movie_release_date = body.get('release_date')

      if movie_title:
        movie.title = movie_title
      if movie_release_date:
        movie.release_date = movie_release_date

      movie.update()

      return jsonify({
        'success': True,
        'actors': [movie.format()]
      })

    except:
      abort(422)



  # =====================================DELETE Requests=====================================

  '''
  @ implement endpoint
    DELETE /actors/<id>
  '''
  @app.route('/actors/<id>', methods=['DELETE'])
  @requires_auth('delete:actors')
  def delete_actors(token, id):
    try:
      actor = Actor.query.filter(Actor.id == id).one_or_none()

      if actor is None:
        abort(404)

      actor.delete()

      return jsonify({
        'success': True,
        'delete': id
      })

    except:
      abort(422)


  '''
  @ implement endpoint
    DELETE /movies/<id>
  '''
  @app.route('/movies/<id>', methods=['DELETE'])
  @requires_auth('delete:movies')
  def delete_movies(token, id):
    try:
      movie = Movie.query.filter(Movie.id == id).one_or_none()

      if movie is None:
        abort(404)

      movie.delete()

      return jsonify({
        'success': True,
        'delete': id
      })

    except:
      abort(422)



  # =====================================Error Handlers=====================================

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False, 
      "error": 422,
      "message": "unprocessable"
    }), 422

  @app.errorhandler(404)
  def resource_not_found(error):
    return jsonify({
      "success": False, 
      "error": 404,
      "message": "resource not found"
    }), 404

  @app.errorhandler(401)
  def unauthorized(error):
    return jsonify({
      "success": False,
      "error": 401,
      "message": 'unauthorized'
    }), 401

  @app.errorhandler(500)
  def internal_server_error(error):
    return jsonify({
      "success": False,
      "error": 500,
      "message": 'internal server error'
    }), 500

  @app.errorhandler(AuthError)
  def auth_error(error):
    return jsonify({
      "success": False, 
      "error": error.status_code,
      "message": error.error['description']
    }), error.status_code


  return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)