"""CSC110 Fall 2021 Project Phase 2: The Main File

File Instructions
===============================
This file contains a single initialization function that is automatically run when the file is run,
which prompts the user on what graph they would like, followed by their datatype location. Location
must be written with .csv at the end

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of TA's and professors
working at CSC110 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are...
not really minded. Please do credit though!

This file is Copyright (c) 2021 Madhav Kanna Thenappan, Prahlad Ranjit, Amirali Tolooei,
and Vinayak Maharaj.
"""
# import python_ta

import mental_health
import unemployment
import covid


def initialize_program() -> None:
    """This function allows users to enter answers to prompts which while execute an if statement
    depending on the value of the input. Each if statement will run a different function leading to
    the creation of a graph.
    """
    print("The graphs available to plot are: \n 1. unemployment \n 2. unemployment regression"
          "\n 3. covid \n 4. covid regression"
          "\n 5. mental health bar \n 6. mental health pie \n (please enter options as is, "
          "eg: What Graph Would You Like? \n >? covid 19)")
    graph_type = input('What Graph Would You like?')
    if graph_type.lower() == 'unemployment':
        data_file = input(r'Please input your data file location')
        data_location = fr'{data_file}'
        graphing_data = unemployment.create_data(data_location)
        unemployment.graph_data(graphing_data)
    elif graph_type.lower() == 'unemployment regression':
        data_file = input(r'Please input your data file location')
        data_location = fr'{data_file}'
        graphing_data = unemployment.create_data(data_location)
        unemployment.unemployment_regression(graphing_data)
    elif graph_type.lower() == 'covid':
        data_file = input('Please input your data file location (with .csv at the end)')
        data_location = fr'{data_file}'
        graph = covid.Covid()
        graph.load_data(data_location)
        covid.plot_data(graph.all_data)
    elif graph_type.lower() == 'covid regression':
        data_file = input('Please input your data file location (with .csv at the end)')
        data_location = fr'{data_file}'
        graph = covid.Covid()
        graph.load_data(data_location)
        covid.graph_regression(graph.regression_ratio, graph.all_data)
    elif graph_type.lower() == 'mental health bar':
        data_file = input('Please input your data file location')
        data_location = fr'{data_file}'
        mh = mental_health.MentalHealth()
        mh.load_data(data_location)
        mental_health.bar_graph_mental_health(mh.all_data)
    elif graph_type.lower() == 'mental health pie':
        data_file = input('Please input your data file location')
        data_location = fr'{data_file}'
        mh = mental_health.MentalHealth()
        mh.load_data(data_location)
        mental_health.pie_chart_mental_effect(mh.all_data)
    elif graph_type.lower() == 'exit':
        return None
    else:
        print('Not a valid input, please try again')
        initialize_program()
    return None


initialize_program()

# python_ta.check_all(config={
#     'extra-imports': ['mental_health', 'unemployment', 'covid'],
#     # the names (strs) of imported modules
#     'allowed-io': ['initialize_program'],
#     # the names (strs) of functions that call print/open/input
#     'max-line-length': 100,
#     'disable': ['R1705', 'C0200']
# })
