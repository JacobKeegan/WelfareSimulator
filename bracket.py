"""
Contains a class representing a bracket for taxes or welfare benefits, and a function using those brackets to calculate
those taxes or welfare benefits.
"""
from collections import namedtuple

from typing import List

Bracket = namedtuple("Bracket", "start, end, rate")


# Takes in a list of change points (where a bracket changes) and a list of rates, and returns a list of brackets.
# Removes having to duplicate the end of one brackets and the start of another.
def make_brackets(change_points: list, rates: list) -> List[Bracket]:
    if len(change_points) < 2:
        raise Exception("Error! Number of change points for a bracket must be >= 2.")
    if len(change_points)-len(rates) != 1:
        raise Exception("Error! There must be exactly one more change point than there are rates.")
    brackets = []
    for i in range(len(rates)):
        brackets.append(Bracket(change_points[i], change_points[i+1], rates[i]))
    return brackets


# Takes in an income and a tax or welfare benefit. Returns the size of the tax or welfare benefit.
# Taxes and welfare benefits are composed of a list of Brackets.
def get_taxfare(income, taxfare: List[Bracket]):
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
