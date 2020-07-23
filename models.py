from datetime import datetime
import json

from pyramid.security import Allow, Everyone

from sqlalchemy import (
    Column,
    Integer,
    Text,
    DateTime
    )

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import as_declarative

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import register

DBSession = scoped_session(sessionmaker())
register(DBSession)
Base = declarative_base()


class Record(Base):
    __tablename__ = 'Records'
    uid = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, unique=True, default=datetime.utcnow)
    bp_upper = Column(Integer)
    bp_lower = Column(Integer)
    notes = Column(Text)

    def to_dict(self):
        return {
            "uid": self.uid,
            "timestamp": self.timestamp.isoformat(),
            "bp_upper": self.bp_upper,
            "bp_lower": self.bp_lower,
            "notes": self.notes
            }

    def to_json(self):
        return json.dumps(self.to_dict())


class Root(object):
    __acl__ = [(Allow, Everyone, 'view'),
               (Allow, 'group:editors', 'edit')]

    def __init__(self, request):
        pass