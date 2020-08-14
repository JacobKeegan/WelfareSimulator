from filing_status import *


class TaxUnit:
    def __init__(self, income, num_kids, filing_status: FilingStatus):
        self.income = income  # you could prob add deductions here if u want
        self.num_kids = num_kids
        self.filing_status = filing_status
        self.base_income_taxes = None
