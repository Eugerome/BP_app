"""BP api views."""

import logging
import transaction

from pyramid.response import Response

from pyramid.view import view_config, view_defaults

from models import DBSession, Record

logger = logging.getLogger(__name__)

# pylint: disable=E1101
@view_defaults(renderer="json")
class BpApiViews:
    """API views that generate/display records."""

    def __init__(self, request):
        self.request = request

    @view_config(route_name="home")
    def home(self):  # pylint: disable=R0201
        """Simple method for debugging issues."""
        logger.info("Home view")
        return {"name": "Home View"}

    @view_config(route_name="records", request_method="GET")
    def return_records(self):  # pylint: disable=R0201
        """Returns all records in the database."""
        logger.info("Return records")
        records = DBSession.query(Record).all()
        if records:
            records_json = []
            for record in records:
                records_json.append(record.to_dict())
            return records_json
        return {"success": False}

    @view_config(route_name="add_record", request_method="POST")
    def add_record(self):
        """Verifies post form and saves record to database."""
        form_json = self.request.json
        with transaction.manager:
            record = Record.from_dict(form_json)
            DBSession.add(record)
            transaction.commit()
        return Response(status=201)

    @view_config(route_name="operate_record", request_method="GET")
    def get_record(self):
        """Retrieve record based on id."""
        record_id = self.request.matchdict["id"]
        # shouldn't be any duplicate id since primary key
        record = DBSession.query(Record).filter_by(id=record_id).first()
        if record:
            return record.to_dict()
        return Response(status=404)

    @view_config(route_name="operate_record", request_method="PUT")
    def update_record(self):
        """Update record based on id."""
        form_json = self.request.json
        record_id = self.request.matchdict["id"]
        # shouldn't be any duplicate id since primary key
        record = DBSession.query(Record).filter_by(id=record_id).first()
        if record:
            for key, value in form_json.items():
                setattr(record, key, value)
            transaction.commit()
            return Response(status=200)
        return self.add_record()

    @view_config(route_name="operate_record", request_method="DELETE")
    def delete_record(self):
        """Delete record based on id."""
        record_id = self.request.matchdict["id"]
        # shouldn't be any duplicate id since primary key
        record = DBSession.query(Record).filter_by(id=record_id).first()
        if record:
            with transaction.manager:
                DBSession.delete(record)
                transaction.commit()
            return Response(status=202)
        return Response(status=204)
