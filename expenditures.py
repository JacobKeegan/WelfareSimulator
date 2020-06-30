from bracket import *
from data import CTC, adult_EITC, child_EITC


def get_total_taxfare(income, num_adults, num_children):
    # get normal income taxes
    # get refundable and non-refundable welfare
    pass


def get_CTC(income, tax_burden):
    benefit = get_taxfare(CTC, income)
    if benefit <= tax_burden:
        tax_burden -= benefit
    else:
        non_refundable = tax_burden
        tax_burden = 0
        refundable = min(1400, benefit-non_refundable)
        refundable = min(refundable, .15*(income-2500))

