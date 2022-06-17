"""CSC110 Fall 2021 Project Phase 2: Unemployment Graphing

File Instructions
===============================
This file contains methods that extract, clean and format data from the source unemployment data
csv files as well as plot the data on either a line graph or a regression line graph depending on
which function is called in main.py

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of TA's and professors
working at CSC110 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are...
not really minded. Please do credit though!

This file is Copyright (c) 2021 Madhav Kanna Thenappan, Prahlad Ranjit, Amirali Tolooei,
and Vinayak Maharaj.
"""

import csv
import matplotlib.pyplot as plt
import pandas as pd
# import python_ta


def create_data(file: str) -> list:
    """Loads the unemployment rate data from datafile starting at March 2020 and returns a list
    consisting of a list of the dates, a list of the unemployment percentages, and the value
    of the average slope between the points

    Also creates a regression variable (regression_slope) which will correspond to the slope of all
    data provided and the total average slope of the graphs

    >>> x = create_data(r'dataset.csv') #any non empty csv dataset formatted in the required format
    >>> x != []
    True
    """
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader)

        months = ['3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
        month_starts = ['0', '1', '2']
        unemployment_percentages = []
        dates = []
        regression_slope = 0
        number_of_points = 0
        previous_number = 0
        for row in csv_reader:
            if ('2020' in row[0] and row[0][6] in months) or \
               ('2020' in row[0] and row[0][6] in month_starts and row[0][5] == '1') or \
               '2021' in row[0]:
                unemployment_percentages.append(float(row[1]))
                dates.append(row[0])
                if number_of_points >= 0:
                    regression_slope += (float(row[1]) - previous_number)
                number_of_points += 1
            previous_number = float(row[1])

        regression_slope = regression_slope / (number_of_points - 1)

        return [dates, unemployment_percentages, regression_slope]


def graph_data(converted_data: list) -> None:
    """Plots the data on a line graph modeling time (x-axis) to unemployment percentages (y-axis) on
    top of formatting the graph with corresponding labels


    Preconditions:
        - Every value in converted_data[0] has a unique date
        - converted_data != []
        - converted_data[0] != []
        - len(converted_data[0]) == len(converted_data[1])

    """
    usable_data = pd.DataFrame({'date': converted_data[0], 'unemployment_rates': converted_data[1]})
    usable_data['date'] = pd.to_datetime(usable_data['date'])
    usable_data.set_index('date')['unemployment_rates'].plot()
    plt.xlabel("Date", labelpad=15)
    plt.ylabel("Unemployment Percentages (%)", labelpad=15)
    plt.title("Unemployment Rates Through Time", y=1.02)


def unemployment_regression(converted_data: list) -> None:
    """Draws out the regression model of the provided data modeling time (x-axis) to
    unemployment percentages (y-axis) on top of formatting the graph with corresponding labels


    Preconditions:
        - Every value in converted_data[0] has a unique date
        - converted_data[0] != []
        - isinstance(converted_data[2], float) is True

    """
    regression = [converted_data[2]]
    regression_list = []

    for i in range(1, len(converted_data[0]) + 1):
        regression_list.append(regression[0] * i)

    regression_data = pd.DataFrame({'date': converted_data[0],
                                    'unemployment_regression': regression_list})
    regression_data['date'] = pd.to_datetime(regression_data['date'])
    regression_data.set_index('date')['unemployment_regression'].plot()
    plt.xlabel("Date", labelpad=15)
    plt.title("Unemployment Regression", y=1.02)
    plt.ylabel("Unemployment Percentages (%)", labelpad=15)
    plt.show(block=True)


# python_ta.check_all(config={
#     'extra-imports': ['csv', 'matplotlib.pyplot', 'pandas'],  # the names (strs) of imported modules
#     'allowed-io': ['create_data'],  # the names (strs) of functions that call print/open/input
#     'max-line-length': 100,
#     'disable': ['R1705', 'C0200']
# })
