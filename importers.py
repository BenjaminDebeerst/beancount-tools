from csv import Dialect

from beangulp import mimetypes
from beangulp.importers import csvbase

class SemicolonCSV(Dialect):
    delimiter = ';'
    quotechar = '"'
    doublequote = True
    skipinitialspace = False
    lineterminator = '\r\n'
    quoting = 3

class GLSImporter(csvbase.Importer):
    '''
    Importer for GLS Bank.
    '''
    date = csvbase.Date('Buchungstag', '%d.%m.%Y')
    narration = csvbase.Column('Verwendungszweck')
    payee = csvbase.Column('Name Zahlungsbeteiligter')
    amount = csvbase.Amount('Betrag', subs = {',': '.'})

    def __init__(self, target_account, filename_part):
        self.dialect = SemicolonCSV()
        self.importer_account = target_account
        self.currency = 'EUR'
        self.flag = '*'
        self.filename_part = filename_part

    @property
    def name(self):
        return 'GLS Importer for ' + self.filename_part

    def identify(self, filepath):
        mimetype, encoding = mimetypes.guess_type(filepath)
        if mimetype != 'text/csv':
            return False
        else:
            return self.filename_part in filepath
