import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import *
from datetime import date


casting_assistant_header = { 'Authorization': 'Bearer {}'.format(os.environ['CASTING_ASSISTANT_TOKEN']) }
casting_director_header = { 'Authorization': 'Bearer {}'.format(os.environ['CASTING_DIRECTOR_TOKEN']) }
executive_producer_header = { 'Authorization': 'Bearer {}'.format(os.environ['EXECUTIVE_PRODUCER_TOKEN']) }

class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ['TEST_DATABASE_URL']
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    new_actor = {
        'name': 'Test Actor',
        'age': 30,
        'gender': 'Male'
    }

    new_movie = {
        'title': 'Test Movie',
        'release_date': date.today()
    }

    proper_quiz_question = {
        'quiz_category': {
            'type': 'Entertainment',
            'id': 5
        },
        'previous_questions': [2, 6]
    }

    """
    GET test for /actors
    """
    def test_get_actors(self):
        res = self.client().get('/actors', headers = casting_assistant_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_401_get_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header is expected.')

    """
    GET test for /movies
    """
    def test_get_movies(self):
        res = self.client().get('/movies', headers = casting_assistant_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_401_get_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header is expected.')
    
    """
    POST test for /actors
    """
    def test_create_new_actor(self):
        res = self.client().post('/actors', json=self.new_actor, headers = casting_director_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))
        self.assertEqual(data['actors'], self.new_actor)

    def test_401_create_new_actor(self):
        res = self.client().post('/actors', json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header is expected.')

    """
    POST test for /movies
    """
    def test_create_new_movie(self):
        res = self.client().post('/movies', json=self.new_movie, headers = executive_producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))
        self.assertEqual(data['movies'], self.new_movie)

    def test_401_create_new_movie(self):
        res = self.client().post('/movies', json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header is expected.')

    """
    PATCH test for /actors/<id>
    """
    def test_update_actor_age(self):
        res = self.client().patch('/actors/1', json={'age': 100}, headers = casting_director_header)
        data = json.loads(res.data)
        actor = Actor.query.filter(Actor.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(actor.format()['age'], 100)

    def test_422_update_actor(self):
        res = self.client().patch('/actors/1', headers = casting_director_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_404_update_actor_age(self):
        res = self.client().patch('/actors/1000', json={'age': 100}, headers = casting_director_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    """
    PATCH test for /movies/<id>
    """
    def test_update_movie_title(self):
        res = self.client().patch('/movies/1', json={'title': 'Mall Cop'}, headers = casting_director_header)
        data = json.loads(res.data)
        movie = Movie.query.filter(Movie.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(movie.format()['title'], 'Mall Cop')

    def test_422_update_movie(self):
        res = self.client().patch('/movies/1', headers = casting_director_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_404_update_movie_title(self):
        res = self.client().patch('/movies/1000', json={'title': 'Mall Cop'}, headers = casting_director_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    """
    DELETE test for /actors
    """
    def test_delete_actor(self):
        res = self.client().delete('/actors/2', headers = casting_director_header)
        data = json.loads(res.data)

        actor = Actor.query.filter(Actor.id == 2).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 2)
        self.assertEqual(actor, None)

    def test_404_delete_actor(self):
        res = self.client().delete('/actors/1000', headers = casting_director_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_403_delete_actor(self):
        res = self.client().delete('/actors/2', headers = casting_assistant_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found')

    """
    DELETE test for /movies
    """
    def test_delete_movie(self):
        res = self.client().delete('/movies/2', headers = executive_producer_header)
        data = json.loads(res.data)

        movie = Movie.query.filter(Movie.id == 2).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 2)
        self.assertEqual(movie, None)

    def test_404_delete_actor(self):
        res = self.client().delete('/actors/1000', headers = executive_producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_403_delete_actor(self):
        res = self.client().delete('/actors/2', headers = casting_director_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
