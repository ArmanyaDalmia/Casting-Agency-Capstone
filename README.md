# Casting Agency Capstone

## Casting Agency Specifications

The Casting Agency application is the capstone project for the Udacity Full Stack Nanodegree Course and is an API for managing the actors and movies of a casting agency. This API was built using/following:

1) RESTful principles to carry out CRUD operation through Flask
2) Data modeling using SQLAlchemy with a Postgres backend (on local machine and Heroku)
3) Third-Party Authentication facilitated through Auth0
4) Automated testing through Unittest
5) The API is hosted live through Heroku

Heroku Link: [https://fsnd-casting-agency-capstone.herokuapp.com/](https://fsnd-casting-agency-capstone.herokuapp.com/)

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

Working within a virtual environment is recommended and instructions for setting up a virual enviornment can be found [here](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages within the `requirements.txt` file.

#### Database Setup

You will need to have PostgreSQL installed. To run the API, you will need to have your Postgres server running and create a database. (Will also need to create another database if you wish to test locally)


#### Environment Variables

Add your database environment variables to the `setup.sh` file by changing `DATABASE_URL` (and `TEST_DATABASE_URL` if appropriate) and then run:

```bash
source setup.sh
```

This will set the environment variables locally.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Running the server

From the root directory, first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

## Testing
First make sure you have created a `postgres` database for the tests.

To run the tests, execute:
```

python test_flaskr.py
```

## API Reference

### Getting Started
- Base URL: This app can be run locally or through the provided `Heroku` link
- Authentication: This app uses Auth0 for authentication. JWT tokens have been provided in the `setup.sh` file and should be available in your local environment if you have completed the steps for Installing Dependencies. These tokens are:
	- CASTING_ASSISTANT_TOKEN
	- CASTING_DIRECTOR_TOKEN
	- EXECUTIVE_PRODUCER_TOKEN

### Roles:
The JWT tokens are associated with Auth0 roles that each have different permissions
- Casting Assistant
	- `get:actors`, `get:movies`
- Casting Director
	- All permissions a Casting Assistant has and…
	- `post:actors`, `delete:actors`
	- `patch:actors`, `patch:movies`
- Executive Producer
	- All permissions a Casting Director has and…
	- `post:movies`, `delete:movies`

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return 5 error types when requests fail:
- 400: Bad Request
- 401: Unauthorized
- 403: Permission not found
- 404: Resource Not Found
- 422: Not Processable

The error messages for error types 400, 401, 403 may differ though these are the standard


### Endpoints

#### GET /actors
- Returns a list of actors 
- Requires the `get:actors` permission

```
{
  'success': True,
  'actors': [
    {
      id: 1,
      name: 'Test Actor',
      age: 30,
      gender: 'Male'
    }
  ]
}
```

#### GET /movies
- Returns a list of movies 
- Requires the `get:movies` permission

```
{
  'success': True,
  'movies': [
    {
      id: 1,
      name: 'Test Movie',
      release_date: '2020-7-30 06:00',
    }
  ]
}
```

#### POST /actors
- Creates a new actor using the provided parameters/arguments
- Requires the `post:actors` permission
- Request Arguments are a json object of the form: { name: String, age: Integer, gender: String }

```
{
  'success': True,
  'actors': [
    {
      id: 2,
      name: 'New Actress',
      age: 30,
      gender: 'Female'
    }
  ]
}
```

#### POST /movies
- Creates a new movie using the provided parameters/arguments
- Requires the `post:movies` permission
- Request Arguments are a json object of the form: { title: String, release_date: Date }

```
{
  'success': True,
  'actors': [
    {
      id: 2,
      title: 'New Movie',
      release_date: '2020-7-30 06:30',
    }
  ]
}
```

#### PATCH /actors/{id}
- Updates an actor using the provided parameters/arguments
- Requires the `patch:actors` permission and the id of the actor to be updated
- Request Arguments are a json object of the form: { name: String, age: Integer, gender: String }

```
{
  'success': True,
  'actors': [
    {
      id: 2,
      name: 'Updated Actress',
      age: 31,
      gender: 'Female'
    }
  ]
}
```

#### PATCH /movies/{id}
- Updates a movie using the provided parameters/arguments
- Requires the `post:movies` permission and the id of the movie to be updated
- Request Arguments are a json object of the form: { title: String, release_date: Date }

```
{
  'success': True,
  'actors': [
    {
      id: 2,
      title: 'Updated Movie',
      release_date: '2021-8-31 06:31',
    }
  ]
}
```

#### DELETE /actors/{id}
- Deletes an actor using the provided parameters/arguments
- Requires the `delete:actors` permission and the id of the actor to be removed
 
```
{
  'success': True,
  'id': '2'
}
```

#### DELETE /movies/{id}
- Deletes a movie using the provided parameters/arguments
- Requires the `delete:movies` permission and the id of the movie to be removed
 
```
{
  'success': True,
  'id': '2'
}
```

## Acknowledgements

The Udacity Full Stack Nanodegree Instructor and Course developers

