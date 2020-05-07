from flask import current_app, url_for
from flask_testing import TestCase
from main import app


class MainTest(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def test_app_exists(self):
        self.assertIsNotNone(current_app)

    def test_app_in_testing(self):
        self.assertTrue(current_app.config['TESTING'])

    def test_index_load(self):
        response = self.client.get('/')
        self.assert200(response)

    def test_signin(self):
        fake_form = {
            'username': 'paulgrimaldo',
            'password': '1234545'
        }

        response = self.client.post(url_for('auth.sign_in'), data=fake_form)
        self.assertRedirects(response, url_for('index'))

    def test_auth_blueprint_exists(self):
        self.assertIn('auth', self.app.blueprints)

    def test_auth_login_get(self):
        response = self.client.get('auth.login')
        self.assert200(response)

    def test_auth_login_template(self):
        self.client.get(url_for('auth.login'))
        self.assertTemplateUsed('login.html')
