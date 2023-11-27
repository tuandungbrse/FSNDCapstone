import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Actors, Movies

class CastingAgencyTestCase(unittest.TestCase):

    def setUp(self):

        DATABASE_URL = 'postgresql://postgres:postgres@localhost:5432/fsnd_test'
        ASSISTANT_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkR1SnhtaW13RERJSV9ZYVhPdDFMViJ9.eyJpc3MiOiJodHRwczovL2Rldi1lcHU4amZrd3N2ZTdpbXVsLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NTY0NjA5MDE3YjRiZGI1MDExNTdjZDAiLCJhdWQiOiJmc25kIiwiaWF0IjoxNzAxMDc3MjQxLCJleHAiOjE3MDExNjM2NDEsImF6cCI6IkllQWMzUjhWbmc4Tm1obzRuVzByU1N2MDNPcGxDdHR2Iiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.WtE3cKCwzBhs3oH-sss-uNXuo6Wmsye_H5Z2lIgEbtL1QX7A_KIDU-RN7S1jhjBgVTgq1h_qw2aoNYuDLB6SO_5G6RyUfHkoODftbGdz3PWwWRRSrinCUP1ZAp3bhpEuwuieEs785OCDoa6qIc72T-Kadto1DsSWnMt0KdnT3wo9AgdSEZmCt0qaxqMxjeWqiu5_tTjvZDX9a880gTeDSlASzSKhfRRGSEubImvMboQCWbOYyIBXRVVu8XW2QiBWkb0cSUa4IVWqDS5jHAVB8ku6FOPppe2UdifbmnXD-FYEZM7m5Wp21UB4_b2sRLtzFBoCCLGaUXJvsSd2oVfE4g'
        DIRECTOR_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkR1SnhtaW13RERJSV9ZYVhPdDFMViJ9.eyJpc3MiOiJodHRwczovL2Rldi1lcHU4amZrd3N2ZTdpbXVsLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NTY0NjMxOTMxMTA4ZmQxYmExZDU5NmQiLCJhdWQiOiJmc25kIiwiaWF0IjoxNzAxMDc4MTAxLCJleHAiOjE3MDExNjQ1MDEsImF6cCI6IkllQWMzUjhWbmc4Tm1obzRuVzByU1N2MDNPcGxDdHR2Iiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.WYHX4mPd-xK4t0XUM5zbdtF-VlIf46Yw_lf1GbmgDqDjN8R85CDd_mgKUNo2n4qlOlD8UeSPJjqYKwOIxjpDY0FCSSO_88PZktePPuV2HQ0gjoK7a-r-UkbgDhrGhpK7hNzm9LsNbpPmOsG2LW-mJZX3fKrZPCmgvz-7SZ-82a8bVaVDQD7PyTYgNtRPrEnnlP4bXFi5ZF4HwAB5lHCgrvY21FSwa1Gb7vWEEGtkbTFveXH20Fn94uXqFwRRsiz_PmGtMdNCbi6lQTNu6UFXXOG_0w5QxTYc9eTK_8H0IpYY1P5wPQo9tt7BlRQttx1E9ytpUHCVNJ7NIqMeI5FdDg'
        PRODUCER_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkR1SnhtaW13RERJSV9ZYVhPdDFMViJ9.eyJpc3MiOiJodHRwczovL2Rldi1lcHU4amZrd3N2ZTdpbXVsLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NTY0NjU2YTMxMTA4ZmQxYmExZDViZTIiLCJhdWQiOiJmc25kIiwiaWF0IjoxNzAxMDc4NDEyLCJleHAiOjE3MDExNjQ4MTIsImF6cCI6IkllQWMzUjhWbmc4Tm1obzRuVzByU1N2MDNPcGxDdHR2Iiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.BVeDF5TKBPgCBPwXOM2PmVycbuFRpPspdsn3E2-ny3LmV60UY0b_Ydl1CWObtoXHP8h7k1gcIGvUA3GZxE-mjG1F3ExS-9fDcl6tqfprK9cOMzUj22tGswAf2P9G9pzRNXWuhKCacJPfCTQNbB6kN9SF961ketGOyRK7uNAob_RVGEoEe4BSwHQleuuKq1PCDb97_KfnQ3mp9A0A2YkG4wvQ3njl0Fb2_TE-PVBf28YkY4lOr9f1SvUY8wh1JQ7sj139OGRQVEiC6wYji_nJCLdYMK-hyiOQnn7s4iFJhoz8VE0iXdNQ8i8XmJU0pTQ5xYxh4v9uYa8qzsie1q2CRA'

        self.assistant_auth_header =  {'Authorization': 'Bearer ' + ASSISTANT_TOKEN}
        self.director_auth_header  =  {'Authorization': 'Bearer ' + DIRECTOR_TOKEN}
        self.producer_auth_header  =  {'Authorization': 'Bearer ' + PRODUCER_TOKEN}
        self.database_path = DATABASE_URL

        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app, self.database_path)

        self.post_actor = {
            'name': "Mike",
            'age': 25,
            'gender': 'MALE'
        }

        self.post_actor1 = {
            'name': "George",
            'age': 28,
            'gender': 'MALE'
        }

        self.post_actor2 = {
            'name': "Markus",
            'age': 39,
            'gender': 'MALE'
        }

        self.post_actor_name_missing = {
            'age': 34,
            'gender': "MALE"
        }

        self.post_actor_gender_missing = {
            'age': 34,
            'name': "John"
        }

        self.patch_actor_on_age = {
            'age': 55
        }

        self.post_movie = {
            'title': "SAMPLE MOVIE",
            'release_date': "2090-10-10"
        }

        self.post_movie1 = {
            'title': "MAHABHARATA",
            'release_date': "2030-10-10"
        }

        self.post_movie2 = {
            'title': "MAHABHARATA - 2",
            'release_date': "2032-10-10"
        }

        self.post_movie_title_missing = {
            'release_date': "2030-10-10"
        }

        self.post_movie_reldate_missing = {
            'title': "RAMAYANA"
        }

        self.patch_movie_on_reldate = {
            'release_date': "2035-10-10"
        }

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        pass

    def test_assistant_get_actors_success(self):
        res = self.client().get('/actors?page=1', headers=self.assistant_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['actors']) > 0)

    def test_director_get_actors_success(self):
        res = self.client().get('/actors?page=1', headers=self.director_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['actors']) > 0)

    def test_producer_get_actors_success(self):
        res = self.client().get('/actors?page=1', headers=self.producer_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['actors']) > 0)

    def test_director_post_new_actor_success(self):
        res = self.client().post('/actors', json=self.post_actor1, headers=self.director_auth_header)
        data = json.loads(res.data)
        actor = Actors.query.filter_by(id=data['inserted']).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsNotNone(actor)

    def test_producer_post_new_actor_success(self):
        res = self.client().post('/actors', json=self.post_actor2, headers=self.producer_auth_header)
        data = json.loads(res.data)
        actor = Actors.query.filter_by(id=data['inserted']).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsNotNone(actor)

    def test_director_post_new_actor_name_missing(self):
        res = self.client().post('/actors', json=self.post_actor_name_missing, headers=self.director_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'unprocessable')

    def test_director_post_new_actor_gender_missing(self):
        res = self.client().post('/actors', json=self.post_actor_gender_missing, headers=self.director_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'unprocessable')

    def test_director_delete_actor(self):
        res = self.client().post('/actors', json=self.post_actor, headers=self.director_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        actor_id = data['inserted']

        res = self.client().delete('/actors/{}'.format(actor_id), headers=self.director_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], actor_id)

    def test_director_delete_actor_not_found(self):
        res = self.client().delete('/actors/999',headers=self.director_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Not found')

    def test_director_patch_actor(self):
        res = self.client().patch('/actors/2', json=self.patch_actor_on_age, headers=self.director_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['updated'], 2)

    def test_director_patch_actor_not_found(self):
        res = self.client().patch('/actors/99', json=self.patch_actor_on_age, headers=self.director_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Not found')

    def test_get_actors_no_auth(self):
        res = self.client().get('/actors?page=1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'],'Authorization header is expected.')

    def test_assistant_post_actor_failed(self):
        res = self.client().post('/actors', json=self.post_actor1, headers=self.assistant_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Permission not found.')

    def test_assistant_delete_actor_failed(self):
        res = self.client().delete('/actors/10', headers=self.assistant_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Permission not found.')

    def test_assistant_get_movies_success(self):
        res = self.client().get('/movies?page=1', headers=self.assistant_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['movies']) > 0)

    def test_director_get_movies_success(self):
        res = self.client().get('/movies?page=1', headers=self.director_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['movies']) > 0)

    def test_producer_get_movies_success(self):
        res = self.client().get('/movies?page=1', headers=self.producer_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['movies']) > 0)

    def test_producer_post_new_movie_success(self):
        res = self.client().post('/movies', json=self.post_movie2, headers=self.producer_auth_header)
        data = json.loads(res.data)

        movie = Movies.query.filter_by(id=data['inserted']).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsNotNone(movie)

    def test_producer_post_new_movie_title_missing(self):
        res = self.client().post('/movies', json=self.post_movie_title_missing, headers=self.producer_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'unprocessable')

    def test_producer_post_new_movie_reldate_missing(self):
        res = self.client().post('/movies', json=self.post_movie_reldate_missing, headers=self.producer_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'unprocessable')

    def test_producer_delete_movie(self):
        res = self.client().post('/movies', json=self.post_movie, headers=self.producer_auth_header)
        data = json.loads(res.data)
        movie_id = data['inserted']

        res = self.client().delete('/movies/{}'.format(movie_id), headers=self.producer_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['movie-deleted'], movie_id)

    def test_producer_delete_movie_not_found(self):
        res = self.client().delete('/movies/777', headers=self.producer_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Not found')

    def test_director_patch_movie(self):
        res = self.client().patch('/movies/2', json=self.patch_movie_on_reldate, headers=self.director_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['updated'], 2)

    def test_director_patch_movie_not_found(self):
        res = self.client().patch('/movies/99', json=self.patch_movie_on_reldate, headers=self.director_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Not found')

    def test_get_movies_no_auth(self):
        res = self.client().get('/movies?page=1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'authorization_header_missing')

    def test_director_post_movie_failed(self):
        res = self.client().post('/movies', json=self.post_movie1, headers=self.director_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Permission not found')

    def test_director_delete_movie_failed(self):
        res = self.client().delete('/movies/8', headers=self.director_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Permission not found')


if __name__ == "__main__":
    unittest.main()
