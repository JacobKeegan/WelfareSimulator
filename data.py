"""
Contains data about the current US tax & welfare system.
"""
import math
from typing import Dict

from filing_status import *
from bracket import *
from tax_unit import TaxUnit

# Assumes use of standard deduction in 2020.
# TODO: use make_brackets
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
    curr_bracket = Bracket(single[i], single[i + 1], current_rates[i])
    brackets[FilingStatus.SINGLE].append(curr_bracket)
    curr_bracket = Bracket(head_of_household[i], head_of_household[i + 1], current_rates[i])
    brackets[FilingStatus.HEAD_OF_HOUSEHOLD].append(curr_bracket)
    curr_bracket = Bracket(married[i], married[i + 1], current_rates[i])
    brackets[FilingStatus.MARRIED].append(curr_bracket)

# 2020 data for welfare formulas.
c = 10540
c2 = 14800
married_phaseout_increase = 5890
EITC: Dict[FilingStatus, List[List[Bracket]]] = {}


# Initializes full EITC data.
def init_EITC_brackets():
    for isMarried in [True, False]:
        curr_EITC = [create_EITC_bracket_list(2 * c / 3, 5 * c / 6, [.0765, 0, -.0765], isMarried),
                     create_EITC_bracket_list(c, 11 * c / 6, [.34, 0, -.1598], isMarried),
                     create_EITC_bracket_list(c2, 11 * c / 6, [.4, 0, -.2106], isMarried),
                     create_EITC_bracket_list(c2, 11 * c / 6, [.45, 0, -.2106], isMarried)]
        if isMarried:
            EITC[FilingStatus.MARRIED] = curr_EITC
        else:
            EITC[FilingStatus.SINGLE] = curr_EITC
            EITC[FilingStatus.HEAD_OF_HOUSEHOLD] = curr_EITC


# Creates a list of brackets for one part of the EITC.
def create_EITC_bracket_list(phase_in_stop, phase_out_start, rates: List[int], is_married):
    if is_married:
        phase_out_start += married_phaseout_increase
    maximum_benefit = math.ceil(phase_in_stop * rates[0])
    ending_income = math.floor(math.fabs(maximum_benefit / (10 * rates[2])) * 10)
    return make_brackets([0, phase_in_stop, phase_out_start, ending_income], rates)


init_EITC_brackets()

CTC: Dict[FilingStatus, List[Bracket]] = {FilingStatus.SINGLE: make_brackets([0, 200000, MAX_INCOME], [0, -.05]),
                                          FilingStatus.HEAD_OF_HOUSEHOLD: make_brackets([0, 200000, MAX_INCOME], [0, -.05]),
                                          FilingStatus.MARRIED: make_brackets([0, 400000, MAX_INCOME], [0, -.05])}


# Given a TaxUnit, returns that units' EITC benefit.
def get_EITC(tax_unit: TaxUnit):
    return [get_taxfare(tax_unit.pre_tax_market_income,
                        EITC[tax_unit.filing_status][tax_unit.num_kids]), 0]


# Given a TaxUnit, returns that units' CTC benefit.
def get_CTC(tax_unit: TaxUnit):
    starting_benefit = 2000
    benefit = tax_unit.num_kids * (starting_benefit + get_taxfare(tax_unit.pre_tax_market_income,
                                                                  CTC[tax_unit.filing_status]))
    refundable = 0
    if benefit <= tax_unit.base_income_taxes:
        non_refundable = benefit
    else:
        non_refundable = tax_unit.base_income_taxes
        refundable = min(tax_unit.num_kids * 1400, benefit - non_refundable)
        refundable = min(refundable, .15 * (tax_unit.pre_tax_market_income - 2500))
        refundable = max(refundable, 0)
    return [refundable, non_refundable]
