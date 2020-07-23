from datetime import datetime
import json
import random

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

    def __init__(self, timestamp=datetime.utcnow(), bp_upper=random.randint(100,160), bp_lower=random.randint(50,80), notes="Test"):
        """Create an instance with random values by default."""
        self.timestamp = timestamp
        self.bp_upper = int(bp_upper)
        self.bp_lower = int(bp_lower)
        self.notes = str(notes)

    @classmethod
    def from_dict(cls, form_dict):
        """Create an instance from a dict."""
        return cls(
            timestamp=form_dict.get("timestamp", datetime.utcnow()),
            bp_upper=int(form_dict.get("bp_upper", 0)),
            bp_lower=int(form_dict.get("bp_lower", 0)),
            notes=str(form_dict.get("notes", ""))
            )

    def to_dict(self):
        """Returns instance as dict."""
        return {
            "uid": self.uid,
            "timestamp": self.timestamp.isoformat(),
            "bp_upper": self.bp_upper,
            "bp_lower": self.bp_lower,
            "notes": self.notes
            }

    def to_json(self):
        """Returns instance as json."""
        return json.dumps(self.to_dict())




class Root(object):
    __acl__ = [(Allow, Everyone, 'view'),
               (Allow, 'group:editors', 'edit')]

    def __init__(self, request):
        pass