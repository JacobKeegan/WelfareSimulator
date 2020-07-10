"""
Contains functions to calculate taxes and welfare benefits owed.
"""
from data import *
from filing_status import *
from total_benefit import *

tax_credit_functions = [get_EITC, get_CTC]
tax_unit_to_benefits = {}


def generate_data(max_income, max_kids):
    curr_unit: TaxUnit
    curr_benefit: TotalBenefit
    for income in range(max_income):
        for num_kids in range(max_kids):
            for filing_status in FilingStatus:
                curr_unit = TaxUnit(income, num_kids, filing_status)
                refundable = 0
                non_refundable = 0
                for func in tax_credit_functions:
                    result = func(curr_unit)
                    refundable += result[0]
                    non_refundable += result[1]
                curr_benefit = TotalBenefit(refundable, non_refundable, 0)
                tax_unit_to_benefits[curr_unit] = curr_benefit
