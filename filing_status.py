from enum import Enum


class FilingStatus(Enum):
    SINGLE = 1
    HEAD_OF_HOUSEHOLD = 1.5
    MARRIED = 2


def filing_status_to_string(filing_status: FilingStatus):
    string: str = filing_status.name
    string = string.lower()
    return string.replace("_", " ")
