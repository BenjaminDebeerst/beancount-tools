from csv import Dialect
import re

from beangulp import mimetypes
from beangulp.importers import csvbase

# Copied from beangulp 0.3.0-dev in order to be able to run on a released version
# TODO remove and replace with csvbase.CreditOrDebit once 0.3.0 is released
class CreditOrDebit(csvbase.Column):
    """Specialized Column for positive and negative amounts on separate columns.
    Parse and return the amount present in the credit or debit
    fields. The amount in the debit field is negated before being
    returned. Only one of the two fields may be populated. The parsing
    is done as per the Amount column type.
    Args:
      credit: Column name or index for amount.
      debit: Column name or index for negated amount.
      subs: Dictionary mapping regular expression patterns to
        replacement strings. Substitutions are performed with
        re.sub() in the order they are specified.
      default: Value to return if both fields are empty, if specified.
    """
    def __init__(self, credit, debit, subs=None, default=None):
        super().__init__(credit, debit, default=default)
        self.subs = subs if subs is not None else {}
    def parse(self, credit, debit):
        if credit and debit:
            raise csvbase.ValueError('credit and debit fields cannot be populated ar the same time')
        if not credit and not debit:
            raise csvbase.ValueError('neither credit or debit fields are populated')
        value = credit if credit else debit
        for pattern, replacement in self.subs.items():
            value = re.sub(pattern, replacement, value)
        parsed = csvbase.decimal.Decimal(value)
        return parsed if credit else -parsed

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


class BPGOImporter(csvbase.Importer):
    '''
    Importer for BPGO
    '''
    date = csvbase.Date('Date de comptabilisation', '%d/%m/%Y')
    amount = CreditOrDebit(credit='Credit', debit='Debit', subs = {',': '.', '-': ''})
    narration = csvbase.Columns('Libelle operation', 'Informations complementaires', 'Type operation')

    def __init__(self, target_account):
        self.dialect = SemicolonCSV()
        self.currency = 'EUR'
        self.flag = '*'

        self.importer_account = target_account

    @property
    def name(self):
        return "BPGO"

    _pattern = re.compile('.*\d{8}_\d{7}\.csv')

    def identify(self, filepath):
        mimetype, encoding = mimetypes.guess_type(filepath)
        if mimetype != 'text/csv':
            return False
        else:
            return self._pattern.match(filepath) is not None
