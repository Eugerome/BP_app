"""BP api views."""

import logging
import os
import transaction

import dateutil.parser

from pyramid.response import Response
from pyramid.response import FileResponse

from pyramid.view import view_config, view_defaults

from models import DBSession, Record

logger = logging.getLogger(__name__)

# pylint: disable=E1101
@view_defaults(renderer="json", openapi=True)
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
        if not self.request.params:
            logger.info("Returns all records")
            records = DBSession.query(Record).all()
        else:
            logger.info("Searching records by params")
            for key in self.request.params.keys():
                logger.info("Invalid Query")
                if key not in Record.search_queries:
                    return Response(status=400)
            logger.info("Processing date queries")
            start_date = self.request.params.get("start_date", Record.min_date)
            start_date = Record.get_timestamp(start_date)
            end_date = self.request.params.get("end_date", Record.max_date)
            end_date = Record.get_timestamp(end_date)
            records = (
                DBSession.query(Record)
                .filter(Record.timestamp.between(start_date, end_date))
                .all()
            )
        if records:
            records_json = []
            for record in records:
                records_json.append(record.to_dict())
            return records_json
        return Response(status=204)

    @view_config(route_name="records", request_method="POST")
    def add_record(self):
        """Verifies post form and saves record to database."""
        form_json = self.request.json
        with transaction.manager:
            record = Record.from_dict(form_json)
            DBSession.add(record)
            # refresh record before commit to send creted Record in response
            DBSession.flush()
            DBSession.refresh(record)
            response_json = record.to_json()
            transaction.commit()
        return Response(status=201, json=response_json)

    @view_config(route_name="operate_record", request_method="GET")
    def get_record(self):
        """Retrieve record based on record_id."""
        record_id = self.request.matchdict["record_id"]
        # shouldn't be any duplicate record_id since primary key
        record = DBSession.query(Record).filter_by(record_id=record_id).first()
        if record:
            return record.to_dict()
        return Response(status=404)

    @view_config(route_name="operate_record", request_method="PUT")
    def update_record(self):
        """Update record based on record_id."""
        form_json = self.request.json
        record_id = self.request.matchdict["record_id"]
        # shouldn't be any duplicate record_id since primary key
        record = DBSession.query(Record).filter_by(record_id=record_id).first()
        if record:
            for key, value in form_json.items():
                if key == "timestamp":
                    value = Record.get_timestamp(value)
                setattr(record, key, value)
            response_json = record.to_json()
            transaction.commit()
            return Response(status=200, json=response_json)
        return self.add_record()

    @view_config(route_name="operate_record", request_method="DELETE")
    def delete_record(self):
        """Delete record based on record_id."""
        record_id = self.request.matchdict["record_id"]
        # shouldn't be any duplicate record_id since primary key
        record = DBSession.query(Record).filter_by(record_id=record_id).first()
        if record:
            response_json = record.to_json()
            with transaction.manager:
                DBSession.delete(record)
                transaction.commit()
            return Response(status=202, json=response_json)
        return Response(status=204)


class BpUserViews:
    """API views that generate/display records."""

    def __init__(self, request):
        self.request = request

    @view_config(route_name="record_table", renderer="./templates/table.pt")
    def get_records(self):  # pylint: disable=R0201
        """Simple method for debugging issues."""
        logger.info("Table view")
        return {}
