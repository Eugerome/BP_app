import logging

from pyramid.view import (
    view_config,
    view_defaults
    )

log = logging.getLogger(__name__)

@view_defaults(renderer='./templates/home.pt')
class BP_views:
    def __init__(self, request):
        self.request = request

    @view_config(route_name='home')
    def home(self):
        log.info("Home view")
        return {'name': 'Home View'}

    @view_config(route_name='hello')
    def hello(self):
        log.info("Hello view")
        return {'name': 'Hello View'}