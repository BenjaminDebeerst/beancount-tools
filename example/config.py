from importers import GLSImporter
from importers import BPGOImporter
from importers import INGImporter

CONFIG = [
    GLSImporter('Sample GLS', 'Assets:Sample:One', 'Sample1'),
    BPGOImporter('Assets:Sample:Two'),
    INGImporter('Sample ING', 'Assets:Sample:Three', 'Umsatzanzeige'),
]

