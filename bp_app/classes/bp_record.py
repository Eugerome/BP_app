"""Processes Blood Pressure Data"""
from bp_app.classes.record import Record

class BPRecord(Record):

    def __init__(self):
        super().__init__()
        self.upper = None
        self.lower = None

