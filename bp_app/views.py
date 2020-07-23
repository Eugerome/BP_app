import logging

from pyramid.httpexceptions import HTTPNotFound

from pyramid.view import (
    view_config,
    view_defaults
    )

from models import DBSession, Record

logger = logging.getLogger(__name__)

# @view_defaults(renderer='./templates/home.pt')
@view_defaults(renderer='json')
class BP_views:
    def __init__(self, request):
        self.request = request      

    @view_config(route_name='home')
    def home(self):
        logger.info("Home view")
        return {'name': 'Home View'}

    @view_config(route_name='records', request_method="GET")
    def return_records(self):
        logger.info("Return records")
        # record = Record()
        # DBSession.add(record)
        records = DBSession.query(Record).all()
        if records:
            records_json = []
            for record in records:
                records_json.append(record.to_dict())
            return records_json
        return HTTPNotFound

