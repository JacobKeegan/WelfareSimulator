from data import *


class TaxUnit:
    def __init__(self, income, num_kids, filing_status: FilingStatus):
        self.income = income
        self.num_kids = num_kids
        self.filing_status = filing_status
        self.income_taxes_owed = get_taxfare(brackets[filing_status], income)
