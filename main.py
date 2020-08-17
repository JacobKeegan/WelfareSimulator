from tax_agency import generate_data
from graphing import graph_data


def main():
    max_income = 250000
    step = 10
    max_num_kids = 1
    data = generate_data(max_income, max_num_kids, step)
    graph_data(max_income, data, step, max_num_kids)


if __name__ == "__main__":
    main()
