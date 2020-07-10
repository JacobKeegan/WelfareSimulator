"""
Contains a class representing a bracket for taxes or welfare benefits, and a function using those brackets to calculate
those taxes or welfare benefits.
"""
from collections import namedtuple

Bracket = namedtuple("Bracket", "start, end, rate")


# Takes in an income and a tax or welfare benefit. Returns the size of the tax or welfare benefit.
# Taxes and welfare benefits are composed of a list of Brackets.
def get_taxfare(income, taxfare: list):
    ret = 0
    # A tax or welfare benefit is just a list of brackets.
    for section in taxfare:
        # Get the income that this section is applying to.
        x = min(income, section.end)
        curr = section.rate*(x-section.start)
        ret += curr
        if x == income:
            break
    return ret
