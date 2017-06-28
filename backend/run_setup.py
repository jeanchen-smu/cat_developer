from database import setup
from database.parnter_table import PartnerTable

es = setup.es

# delete all existing tables
setup.delete_all_tables()
setup.create_tables()

# create partners
partner = PartnerTable()
partner.insert(
    'Goldbell', {'PartnerName': 'Goldbell', 'APIAccessCode': 'e62a48f233'})
# partner.insert( 'Goldbell', {'PartnerName': 'Goldbell', 'APIAccessCode': '1009b9a70c'})
es.indices.refresh(index='_all')
