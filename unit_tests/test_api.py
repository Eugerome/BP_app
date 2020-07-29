"""Test Api views."""

import json
import unittest
from datetime import datetime, timedelta
import transaction

from webtest import TestApp

from pyramid.paster import get_app

from sqlalchemy import create_engine
from models import DBSession, Record, Base

from bp_app import main


def init_test_db():
    """Create testing database."""
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    DBSession.configure(bind=engine)
    with transaction.manager:
        model = Record(timestamp=datetime.utcnow(), bp_upper=120, bp_lower=70, notes="")
        DBSession.add(model)  # pylint: disable=E1101
    return DBSession


class ApiTests(unittest.TestCase):
    """Tests for api views."""

    def setUp(self):
        """Start up the app so that tests can send requests to it."""
        app = get_app("development.ini")
        self.session = init_test_db()
        self.testapp = TestApp(app)

    def tearDown(self):
        """Tear down the test database."""
        self.session.remove()

    def test_home(self):
        """Test home view."""
        response = self.testapp.get("/", status=200)
        self.assertEqual("Home View", response.json.get("name"))

    def test_get_record(self):
        """Test get_record."""
        # check record that exists
        response = self.testapp.get("/records/1", status=200)
        self.assertTrue(isinstance(response.json, dict))
        # check record that does not exist
        self.testapp.get("/records/9999", status=404)
        # check non integer?

    def test_get_all_records(self):
        """Test return_records without search query."""
        response = self.testapp.get("/records", status=200)
        self.assertTrue(isinstance(response.json, list))

    def test_add_record(self):
        """Test adding a record."""
        # test successful
        payload = {
            "timestamp": "2001-02-02T17:11:20.919467Z",
            "bp_upper": 100,
            "bp_lower": 40,
        }
        self.testapp.post_json("/records", payload, status=201)
        # test bad format
        payload = {"timestamp": "2001-02-02", "bp_upper": 100, "bp_lower": 40}
        self.testapp.post_json("/records", payload, status=400)

    def test_update_record(self):
        """Test modifying a record."""
        # testing updating a record
        payload = {
            "timestamp": "2001-02-02T17:11:20.919467Z",
            "bp_upper": 300,
            "bp_lower": 40,
        }
        response = self.testapp.put_json("/records/1", payload, status=200)
        response = self.testapp.get("/records/1", status=200)
        self.assertEqual(300, response.json.get("bp_upper"))
        # testing updating a record that does not exist
        self.testapp.put_json("/records/9999", payload, status=201)
        # test bad payload
        payload = {"timestamp": "2001-02-02", "bp_upper": 100, "bp_lower": 40}
        self.testapp.put_json("/records/1", payload, status=400)

    def test_delete_record(self):
        """Test record deletion."""
        # test deleting existing record
        self.testapp.delete("/records/1", status=202)
        # test deleting non-existing record
        self.testapp.delete("/records/1", status=204)

    def test_get_search_records(self):
        """Test return_records with search query."""
        date = datetime.utcnow() + timedelta(hours=1)
        date = Record.get_timestamp(date).isoformat(timespec="seconds")
        # test return records due to end_date
        self.testapp.get("/records?end_date={}Z".format(date), status=200)
        # test return no records due to start date
        self.testapp.get("/records?start_date={}Z".format(date), status=204)
        # test bad date string
        self.testapp.get("/records?start_date=AAAAZ", status=400)
