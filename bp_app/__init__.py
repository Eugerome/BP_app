from pyramid.config import Configurator
from pyramid.authorization import ACLAuthorizationPolicy
import os

from sqlalchemy import engine_from_config

from models import DBSession, Base


def main(global_config, **settings):
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    config = Configurator(settings=settings, root_factory='models.Root')
    config.include('pyramid_chameleon')
    config.add_route('home', '/')
    config.add_route("add_record", "/records/add")
    config.add_route("delete_record", "/records/{uid}/delete")
    config.add_route("update_record", "/records/{uid}/update")
    config.add_route("get_record", "/records/{uid}")
    config.add_route("records", "/records")
    config.scan('.views')
    # add openapi config
    config.include("pyramid_openapi3")
    config.pyramid_openapi3_spec(os.path.join(os.path.dirname(__file__), 'openapi.yaml'))
    config.pyramid_openapi3_add_explorer(route='docs')
    # Pyramid requires an authorization policy to be active.
    config.set_authorization_policy(ACLAuthorizationPolicy())
    # Enable JWT authentication.
    config.include('pyramid_jwt')
    config.set_jwt_authentication_policy('secret')
    return config.make_wsgi_app()