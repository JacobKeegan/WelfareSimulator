"""
Contains data about the current US tax & welfare system.
"""
from filing_status import *
from bracket import *
from tax_unit import TaxUnit
# Assumes use of standard deduction in 2020.
MAX_INCOME = pow(10, 11)  # 100 billion dollars
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
c = 10540
c2 = 14800
adult_EITC = make_brackets([0, 2*c/3, 5*c/6, MAX_INCOME], [.0765, 0, -.0765])
# TODO: EITC_married_phase_out_change = [1]
one_child_EITC = make_brackets([0, c, 11*c/6, MAX_INCOME], [.34, 0, -.1598])
two_child_EITC = make_brackets([0, c2, 11*c/6, MAX_INCOME], [.4, 0, -.2106])
three_child_EITC = make_brackets([0, c2, 11*c/6, MAX_INCOME], [.45, 0, -.2106])

EITC = [adult_EITC, one_child_EITC, two_child_EITC, three_child_EITC]

# TODO: Assumes individual or HoH status. Else, $200k -> $400k
CTC = make_brackets([0, 200000, MAX_INCOME], [0, -.05])

# Given a TaxUnit, returns that units' EITC benefit.
def get_EITC(tax_unit: TaxUnit):
    return [max(0, get_taxfare(tax_unit.pre_tax_market_income,
                        EITC[tax_unit.num_kids])), 0]


# Given a TaxUnit, returns that units' CTC benefit.
def get_CTC(tax_unit: TaxUnit):
    if tax_unit.num_kids == 0:
        return [0, 0]
    starting_benefit = 2000
    benefit = starting_benefit + tax_unit.num_kids*get_taxfare(tax_unit.pre_tax_market_income, CTC)
    refundable = 0
    if benefit <= tax_unit.base_income_taxes:
        non_refundable = benefit
    else:
        non_refundable = tax_unit.base_income_taxes
        refundable = min(tax_unit.num_kids*1400, benefit-non_refundable)
        refundable = min(refundable, .15 * (tax_unit.pre_tax_market_income - 2500))
        refundable = max(refundable, 0)
    return [refundable, non_refundable]
