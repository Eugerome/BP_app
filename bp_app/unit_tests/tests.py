import unittest
import transaction

from datetime import datetime

from pyramid import testing

def _initTestingDB():
    from sqlalchemy import create_engine
    from .models import (
        DBSession,
        Record,
        Base
        )
    engine = create_engine('sqlite://')
    Base.metadata.create_all(engine)
    DBSession.configure(bind=engine)
    with transaction.manager:
        model = Record(timestamp=datetime.utcnow(), bp_upper=120, bp_lower=70, notes='')
        DBSession.add(model)
    return DBSession


class ViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_home(self):
        from bp_app.views import BP_views

        request = testing.DummyRequest()
        inst = BP_views(request)
        response = inst.home()
        self.assertEqual('Home View', response['name'])

    def test_hello(self):
        from bp_app.views import BP_views

        request = testing.DummyRequest()
        inst = BP_views(request)
        response = inst.hello()
        self.assertEqual('Hello View', response['name'])


class HtmlTests(unittest.TestCase):
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