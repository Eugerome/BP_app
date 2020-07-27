"""Record class methods."""

import json
import random
from datetime import datetime
import dateutil.parser

from pyramid.security import Allow, Everyone, Authenticated

from sqlalchemy import Column, Integer, Text, DateTime

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import scoped_session, sessionmaker

from zope.sqlalchemy import register

DBSession = scoped_session(sessionmaker())
register(DBSession)
Base = declarative_base()


class Record(Base):
    """Record database."""

    __tablename__ = "Records"
    record_id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    bp_upper = Column(Integer)
    bp_lower = Column(Integer)
    notes = Column(Text)
    search_queries = ["start_date", "end_date"]
    min_date = dateutil.parser.parse("1970-01-01T00:00:00Z")
    max_date = dateutil.parser.parse("2070-01-01T00:00:00Z")

    def __init__(
        self,
        timestamp=datetime.utcnow(),
        bp_upper=random.randint(100, 160),
        bp_lower=random.randint(50, 80),
        notes="Test",
    ):
        """Create an instance with random values by default."""
        self.timestamp = timestamp
        self.bp_upper = int(bp_upper)
        self.bp_lower = int(bp_lower)
        self.notes = str(notes)

    @classmethod
    def from_dict(cls, form_dict):
        """Create an instance from a dict."""
        timestamp = form_dict.get("timestamp", datetime.utcnow())
        if isinstance(timestamp, str):
            timestamp = dateutil.parser.parse(timestamp)
        return cls(
            timestamp=timestamp,
            bp_upper=int(form_dict.get("bp_upper", 0)),
            bp_lower=int(form_dict.get("bp_lower", 0)),
            notes=str(form_dict.get("notes", "")),
        )

    def to_dict(self):
        """Returns instance as dict."""
        return {
            "record_id": self.record_id,
            "timestamp": self.timestamp.isoformat(),
            "bp_upper": self.bp_upper,
            "bp_lower": self.bp_lower,
            "notes": self.notes,
        }

    def to_json(self):
        """Returns instance as json."""
        return json.dumps(self.to_dict())


class Root:  # pylint: disable=R0903
    """Permissions."""

    __acl__ = [
        (Allow, Authenticated, "read"),
        (Allow, Everyone, "view"),
        (Allow, "group:editors", "edit"),
    ]

    def __init__(self, request):
        pass
