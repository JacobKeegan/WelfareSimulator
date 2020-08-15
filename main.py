from tax_agency import generate_data
from graphing import graph_data


def main():
    max_income = 400000
    step = 10
    data = generate_data(max_income, 1, step)
    graph_data(max_income, data, step)


if __name__ == "__main__":
    main()
