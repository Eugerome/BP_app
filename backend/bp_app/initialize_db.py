"""Creates a sample database."""

import os
import sys
import random
from datetime import datetime, timedelta
import transaction


from sqlalchemy import engine_from_config

from pyramid.paster import get_appsettings, setup_logging

from models import DBSession, Record, Base


def usage(argv):
    """Prints out db genereation messages."""
    cmd = os.path.basename(argv[0])
    print("usage: %s <config_uri>\n" '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):  # pylint: disable=W0102
    """Initial database setup."""
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, "sqlalchemy.")
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    with transaction.manager:
        current_time = datetime.utcnow()
        for i in range(14):
            record = Record()
            record.timestamp = current_time - timedelta(days=i)
            record.bp_upper = random.randint(100, 160)
            record.bp_lower = random.randint(50, 80)
            DBSession.add(record)  # pylint: disable=E1101


if __name__ == "__main__":
    main()
