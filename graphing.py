from typing import Dict, List, Tuple

from tax_unit import *
from total_benefit import *
from graph_type import *

import matplotlib.pyplot as plt

# TODO: remove this when testing is done
types_to_test = [GraphType.REFUNDABLE_TAX_CREDITS_RECEIVED, GraphType.NON_REFUNDABLE_TAX_CREDITS_RECEIVED]
brackets_to_test = [FilingStatus.SINGLE]


def graph_data(max_income: int, data: Dict[TaxUnit, TotalBenefit], step: int, max_num_kids: int):
    map_to_y_coordinates = {}
    filing_status: FilingStatus
    for filing_status in FilingStatus:
        for i in range(max_num_kids+1):
            for graph_type in GraphType:
                map_to_y_coordinates[(filing_status, i, graph_type)] = []
    # Fill in information to plot.
    incomes = []
    for i in range(0, max_income, step):
        incomes.append(i)
    tax_unit: TaxUnit
    for tax_unit in data.keys():
        for graph_type in GraphType:
            key = (tax_unit.filing_status, tax_unit.num_kids, graph_type)
            data_point = 0
            if graph_type is GraphType.INCOME_TAXES_OWED:
                data_point = tax_unit.base_income_taxes
            if graph_type is GraphType.NON_REFUNDABLE_TAX_CREDITS_RECEIVED:
                data_point = data[tax_unit].non_refundable_credits
            if graph_type is GraphType.REFUNDABLE_TAX_CREDITS_RECEIVED:
                data_point = data[tax_unit].refundable_credits
            map_to_y_coordinates[key].append(data_point)
    graph(max_num_kids, incomes, map_to_y_coordinates)


def graph(max_num_kids: int, x_coordinates: List[int],
          y_coordinates_map: Dict[Tuple[FilingStatus, int, GraphType], list]):
    for i in range(max_num_kids+1):
        for filing_status in brackets_to_test:
            for graph_type in types_to_test:
                plt.xlabel("Income ($)")
                plt.ylabel(graph_type_to_string(graph_type) + " ($)")
                title: str = filing_status_to_string(filing_status)
                plt.title("For " + title + " bracket with " + str(i) + " kids")
                plt.grid(True)
                plt.plot(x_coordinates, y_coordinates_map[(filing_status, i, graph_type)])
                plt.show()
