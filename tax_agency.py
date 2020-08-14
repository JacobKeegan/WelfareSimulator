"""
Contains functions to calculate taxes and welfare benefits owed.
"""
from data import *
from filing_status import *
from total_benefit import *

tax_credit_functions = [get_EITC, get_CTC]
tax_unit_to_benefits = {}
tax_unit_to_taxes = {}


# Fills a dictionary with data mapping TaxUnits to their benefits and taxes.
def generate_data(max_income, max_kids):
    curr_unit: TaxUnit
    curr_benefit: TotalBenefit
    for curr_income in range(max_income+1):
        for num_kids in range(max_kids+1):
            for filing_status in FilingStatus:
                curr_unit = TaxUnit(curr_income, num_kids, filing_status)
                curr_unit.base_income_taxes = get_taxfare(curr_income, brackets[filing_status])
                refundable = 0
                non_refundable = 0
                for func in tax_credit_functions:
                    result = func(curr_unit)
                    refundable += result[0]
                    non_refundable += result[1]
                curr_benefit = TotalBenefit(refundable, non_refundable, 0)
                tax_unit_to_benefits[curr_unit] = curr_benefit
# TODO: Add in code for what a UCA and UBI would be. Can then have it auto-generated compared to norm
# (quicker algorithm for this? Start at max benefit and go down?)
