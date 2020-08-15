from tax_unit import *

import matplotlib.pyplot as plt


def graph_data(max_income: int, data: dict, step: int):
    filing_status_to_incomes = {}
    filing_status: FilingStatus
    for filing_status in FilingStatus:
        filing_status_to_incomes[filing_status] = []
    incomes = []
    for i in range(0, max_income, step):
        incomes.append(i)
    tax_unit: TaxUnit
    for tax_unit in data.keys():
        if tax_unit.num_kids is 0:
            filing_status_to_incomes[tax_unit.filing_status].append(tax_unit.base_income_taxes)
    for filing_status in FilingStatus:
        plt.xlabel("Income ($)")
        plt.ylabel("Income taxes owed ($)")
        title: str = filing_status_to_string(filing_status)
        plt.title("Income taxes for " + title + " bracket")
        plt.grid(True)
        plt.plot(incomes, filing_status_to_incomes[filing_status])
        plt.show()
