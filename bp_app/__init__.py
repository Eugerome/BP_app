from pyramid.config import Configurator

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
    config.add_route("records", "/records")
    config.scan('.views')
    return config.make_wsgi_app()