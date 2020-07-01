import unittest

from pyramid import testing


class TutorialViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_home(self):
        from bp_app.views import home

        request = testing.DummyRequest()
        response = home(request)
        # Our view now returns data
        self.assertEqual('Home View', response['name'])

    def test_hello(self):
        from bp_app.views import hello

        request = testing.DummyRequest()
        response = hello(request)
        # Our view now returns data
        self.assertEqual('Hello View', response['name'])


class TutorialFunctionalTests(unittest.TestCase):
    def setUp(self):
        from bp_app import main
        app = main({})
        from webtest import TestApp

        self.testapp = TestApp(app)

    def test_home(self):
        res = self.testapp.get('/', status=200)
        self.assertIn(b'<h1>Hi Home View', res.body)

    def test_hello(self):
        res = self.testapp.get('/howdy', status=200)
        self.assertIn(b'<h1>Hi Hello View', res.body)