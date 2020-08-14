"""
Contains data about the current US tax & welfare system.
"""
from filing_status import *
from bracket import *
from tax_unit import TaxUnit
# Assumes use of standard deduction in 2020.
MAX_INCOME = pow(10, 12)  # 1 trillion dollars
current_rates = [0, .12, .22, .24, .32, .35, .37]
single = [0, 12401, 39476, 84201, 160726, 204101, 306176, MAX_INCOME]
head_of_household = [0, 18650, 52850]
married = []
# Most of the non-single brackets are just functions of the single bracket.
for i in range(head_of_household.__len__(), single.__len__()):
    head_of_household.append(single[i])
for i in range(single.__len__()):
    married.append(2 * single[i] - 1)

brackets = {FilingStatus.SINGLE: [], FilingStatus.HEAD_OF_HOUSEHOLD: [],
            FilingStatus.MARRIED: []}

# Sets up the map from a Filing status to a list of tax Brackets.
for i in range(current_rates.__len__()):
    curr_bracket = Bracket(single[i], single[i+1], current_rates[i])
    brackets[FilingStatus.SINGLE].append(curr_bracket)
    curr_bracket = Bracket(head_of_household[i], head_of_household[i+1], current_rates[i])
    brackets[FilingStatus.HEAD_OF_HOUSEHOLD].append(curr_bracket)
    curr_bracket = Bracket(married[i], married[i+1], current_rates[i])
    brackets[FilingStatus.MARRIED].append(curr_bracket)

# Data for welfare formulas.
adult_EITC_one = Bracket(0, 6978, .0765)
adult_EITC_two = Bracket(adult_EITC_one.end, 8723, 0)
adult_EITC_three = Bracket(adult_EITC_two.end, 15701, -.0765)
adult_EITC = [adult_EITC_one, adult_EITC_two, adult_EITC_three]
# TODO: EITC_married_phase_out_rate = [1]
# Uses the benefit for 1 child, but applied to every child.
# Assumes individual or HoH status. Else would change phase-out.
child_EITC_one = Bracket(0, 10460, .34)
child_EITC_two = Bracket(child_EITC_one.end, 19184, 0)
child_EITC_three = Bracket(child_EITC_two.end, 41439, .1598)
child_EITC = [child_EITC_one, child_EITC_two, child_EITC_three]
# TODO: Eventually, the EITC for multiple children will be added in here.
EITC = [adult_EITC, child_EITC]

# Assumes individual or HoH status. Else, $200k -> $400k
CTC_one = Bracket(0, 200000, 0)
CTC_two = Bracket(CTC_one.end, 240000, -.05)
CTC = [CTC_one, CTC_two]


# Given a TaxUnit, returns that units' EITC benefit.
def get_EITC(tax_unit: TaxUnit):
    total = 0
    for j in range(tax_unit.num_kids+1):
        total += get_taxfare(tax_unit.income, EITC[j])
    return [total, 0]


# Given a TaxUnit, returns that units' CTC benefit.
def get_CTC(tax_unit: TaxUnit):
    benefit = tax_unit.num_kids*get_taxfare(tax_unit.income, CTC)
    refundable = 0
    if benefit <= tax_unit.base_income_taxes:
        non_refundable = benefit
    else:
        non_refundable = tax_unit.base_income_taxes
        refundable = min(tax_unit.num_kids*1400, benefit-non_refundable)
        refundable = min(refundable, .15*(tax_unit.income-2500))
        refundable = max(refundable, 0)
    return [refundable, non_refundable]
