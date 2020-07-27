import colander
import deform
import logging
import transaction

from pyramid.httpexceptions import HTTPNotFound

from pyramid.view import (
    view_config,
    view_defaults
    )

from models import DBSession, Record

logger = logging.getLogger(__name__)

class RecordSchema(colander.MappingSchema):
    bp_upper = colander.SchemaNode(colander.Integer())
    bp_lower = colander.SchemaNode(colander.Integer())
    notes = colander.SchemaNode(colander.String())


# @view_defaults(renderer='./templates/home.pt')
@view_defaults(renderer='json')
class BP_views:
    def __init__(self, request):
        self.request = request      

    @property
    def record_form(self):
        schema = RecordSchema()
        return deform.Form(schema, buttons=('submit',))

    @view_config(route_name='home')
    def home(self):
        logger.info("Home view")
        return {'name': 'Home View'}

    @view_config(route_name='records', request_method="GET")
    def return_records(self):
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
        controls = self.request.POST.items()
        try:
            form_dict = self.record_form.validate(controls)
        except deform.ValidationFailure as e:
            # Form is NOT valid
            return {"error": "failed to validate"}
        with transaction.manager:
            record = Record.from_dict(form_dict)
            DBSession.add(record)
            transaction.commit()
        return {"success": True}
        
    @view_config(route_name="operate_record", request_method="GET")
    def get_record(self):
        """Retrieve record based on id."""
        id = self.request.matchdict['id']
        # shouldn't be any duplicate id since primary key
        record = DBSession.query(Record).filter_by(id=id).first()
        if record:
            return record.to_dict()
        return {"success": False}

    @view_config(route_name="operate_record", request_method="PUT")
    def update_record(self):
        """Update record based on id."""
        controls = self.request.POST.items()
        try:
            form_dict = self.record_form.validate(controls)
        except deform.ValidationFailure as e:
            # Form is NOT valid
            return {"error": "failed to validate"}
        id = self.request.matchdict['id']
        # shouldn't be any duplicate id since primary key
        record = DBSession.query(Record).filter_by(id=id).first()
        if record:
            for key, value in form_dict.items():
                setattr(record, key, value)
            transaction.commit()
            return {"success": True}
        return {"success": False}

    @view_config(route_name="operate_record", request_method="DELETE")
    def delete_record(self):
        """Delete record based on id."""
        id = self.request.matchdict['id']
        # shouldn't be any duplicate id since primary key
        record = DBSession.query(Record).filter_by(id=id).first()
        if record:
            with transaction.manager:
                DBSession.delete(record)
                transaction.commit()
            return {"success": True}
        return {"success": False}