"""CSC110 Fall 2021 Project Phase 2: Covid Graphing

File Instructions
===============================
This file contains methods that extract, clean and format data from the source csv (covid data)
files as well as plot the data on either a line graph or a regression line graph depending on
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
import pandas as pd
import matplotlib.pyplot as plt
# import python_ta


class Covid:
    """Extracts and stores covid-19 data from file given to it

    Instance Attributes:
     - all_data: a dictionary containing date mapped to number of cases
     - regression_ratio: regression slope variable corresponding to slope of all data and total
     average slope of all the graphs
    """
    all_data: dict[str: int]
    regression_ratio: float

    def __init__(self) -> None:
        """Initializes the instance attributes for Covid class
        """
        self.all_data = {}

    def load_data(self, file: str) -> None:
        """"Loads all data from the given csv file to the datatype Covid"""

        with open(file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader)
            parsed_data = {}
            raw_data = [x for x in csv_reader if x[2] == 'Canada']
            regression_slope = 0
            number_of_points = 0
            previous_number = 0
            months = ['3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
            month_starts = ['0', '1', '2']

            for row in raw_data:
                case_data = (int(row[5]))
                raw_time = row[3]
                time_data = pd.to_datetime(raw_time)
                if ('2020' in raw_time and raw_time[6] in months) or \
                   ('2020' in raw_time and raw_time[6] in month_starts and raw_time[5] == '1') or \
                   '2021' in raw_time:
                    parsed_data[time_data] = case_data
                    if number_of_points >= 0:
                        regression_slope += (int(row[5]) - previous_number)
                        number_of_points += 1
                    previous_number = int(row[5])

            regression_slope = regression_slope / (number_of_points - 1)

        self.all_data = parsed_data
        self.regression_ratio = regression_slope


def plot_data(data: dict) -> None:
    """
    Plots the data on a linear graph modeling time to covid cases

    Preconditions:
     - all(type(date) == datetime.datetime for date in data.keys())
     - all(type(cases) == int for cases in data.values())

    """
    covid_cases = pd.DataFrame({'date': data.keys(), 'cases': data.values()})
    covid_cases['date'] = pd.to_datetime(covid_cases['date'])
    covid_cases.set_index('date')['cases'].plot()
    covid_cases.set_index('date')['cases'].plot(figsize=(12, 10), linewidth=2.5, color='maroon')
    plt.xlabel("Date", labelpad=15)
    plt.ylabel("Covid Cases", labelpad=15)
    plt.title("Covid-19 Cases Throughout the Pandemic", y=1.02)
    plt.show()


def graph_regression(regression: float, data: dict) -> None:
    """Draws out the regression model of the provided data modeling time to covid cases

    Preconditions:
     - all(type(date) == datetime.datetime for date in data.keys())
     - all(type(cases) == int for cases in data.values())
    """
    regression = [regression]
    regression_list = []

    for i in range(1, len(data) + 1):
        regression_list.append(regression[0] * i)

    regression_data = pd.DataFrame({'date': data.keys(),
                                    'confirmed_cases_regression': regression_list})
    regression_data.set_index('date')['confirmed_cases_regression'].plot()
    plt.xlabel("Date", labelpad=15)
    plt.title("Covid Cases Regression", y=1.02)
    plt.ylabel("Covid Cases", labelpad=15)
    plt.show(block=True)


# python_ta.check_all(config={
#     'extra-imports': ['csv', 'matplotlib.pyplot', 'pandas'],  # the names (strs) of imported modules
#     'allowed-io': ['load_data'],  # the names (strs) of functions that call print/open/input
#     'max-line-length': 100,
#     'disable': ['R1705', 'C0200']
# })
