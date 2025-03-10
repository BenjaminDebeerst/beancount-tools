from importers import GLSImporter
from importers import BPGOImporter
from importers import INGImporter
from importers import RegExCategorizer

CONFIG = [
    GLSImporter('Sample GLS', 'Assets:Sample:One', 'Sample1'),
    BPGOImporter('Assets:Sample:Two'),
    INGImporter('Sample ING', 'Assets:Sample:Three', 'Umsatzanzeige'),
]

categorizer = RegExCategorizer([
    ('Paycheck Workplace', 'Income:Salary'),
    ('Rent', 'Expenses:Sample:Rent'),
    ('Supermarket', 'Expenses:Sample:Groceries')
])

for importer in CONFIG:
    importer.finalize = categorizer.run

