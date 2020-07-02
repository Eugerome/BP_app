"""Record class that handles timestamps and reading/writing from db"""
from datetime import datetime

class Record:

    def __init__(self):
        self.created = datetime.utcnow()
        self.last_modified = datetime.utcnow()
        self.additional_info = {}

    def write(self):
        pass

    def read(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass