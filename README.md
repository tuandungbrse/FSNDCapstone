## Getting Started

### Installing Dependencies

#### Python 3.9.18

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

I recommend working within a virtual environment whenever using Python for projects. This keeps dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for the platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```bash
$ pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

#### Running the server

first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
$ source setup.sh
$ export FLASK_APP=app.py
$ export FLASK_ENV=development
$ flask run
```

Sourcing `setup.sh` sets some environment variables used by the app.

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `app.py` directs flask to use the this file to find the application.

## Models:

- **Movies** model defined with attributes title and release date
- **Actors** model defined with attributes name, age and gender

You can find the models in `models.py` file. Local Postgres **DATABASE** details are available in `setup.sh` file for reference.

## Endpoints:

```python
GET /actors &  /movies
DELETE /actors/<int:id> & /movies/<int:id>
POST /actors & /movies
PATCH /actors/<int:id> & /movies/<int:id>
```

All below Endpoints have been created, please refer `app.py` file.

## Auth0 Setup:

**AUTH0_DOMAIN**, **ALGORITHMS** and **API_AUDIENCE** are all available in the `setup.sh` file for reference.
Json Web Tokens: You can find **JWTs** for each role in the `setup.sh` file to run the app locally.

**Roles**: All 3 roles have been defined in Auth0 and following permissions as shown for each role below are also defined in Auth0.

- **Casting Assistant** \* get:actors and get:movies
- **Casting Director**
  _ All permissions a Casting Assistant has and
  _ post:actors and delete:actors \* patch:actors and patch:movies
- **Executive Producer**
  _ All permissions a Casting Director has and
  _ post:movies and delete:movies

## Deployment Details:

- App is deployed in Render Cloud: https://fsnd-web.onrender.com
- To test the application in Render Cloud - import Postman collections & environments included in the repo.

## Testing:

We can run our entire test case by running the following command at command line

```python
$ dropdb fsnd
$ createdb fsnd
$ flask db init
$ flask db migrate
$ flask db upgrade
$ python test_app.py
```
