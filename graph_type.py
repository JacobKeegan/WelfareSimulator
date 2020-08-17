from enum import Enum


class GraphType(Enum):
    INCOME_TAXES_OWED = 1
    REFUNDABLE_TAX_CREDITS_RECEIVED = 2
    NON_REFUNDABLE_TAX_CREDITS_RECEIVED = 3
    CASH_RECEIVED = 4


def graph_type_to_string(graph_type: GraphType):
    string: str = graph_type.name
    string = string.lower()
    return string.replace("_", " ")
