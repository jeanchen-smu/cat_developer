from database.base_table import BaseTable

class PartnerTable(BaseTable):
    def __init__(self):
        BaseTable.__init__(self, 'PARTNER')