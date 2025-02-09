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

    def __init__(self, name, target_account, filename_part):
        self.dialect = SemicolonCSV()
        self.currency = 'EUR'
        self.flag = '*'

        self.importer_account = target_account

        self._name = name
        self._filename_part = filename_part

    @property
    def name(self):
        return self._name

    def identify(self, filepath):
        mimetype, encoding = mimetypes.guess_type(filepath)
        if mimetype != 'text/csv':
            return False
        else:
            return self._filename_part in filepath
