"""CSC110 Fall 2021 Project Phase 2: Mental Health Graphing

File Instructions
===============================
This file contains methods that extract, clean and format data from the source csv files, as well as
plot the the extracted data in multiple bar graph and pie graph

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
import pandas
import matplotlib.pyplot as plt
# import python_ta


class MentalHealth:
    """
    Extract and stores mental health data from file given to it

    Instance Attributes:
     - all_data: all data for respondents
    """
    all_data: list[dict[str, list]]

    def __init__(self) -> None:
        """
        Initializes the instance attributes for MentalHealth class
        """
        self.all_data = [{}]

    def load_data(self, file: str) -> None:
        """"
        Load all data from the given csv file to the datatype MentalHealth
        """
        # all response variables starting with MH are related to mental health
        # all response variable starting with LM are related to labour market
        mh_5_responses = {'Excellent': 1, 'Very good': 2, 'Good': 3, 'Fair': 4, 'Poor': 5}
        mh_10_responses = {'Much better now': 1, 'Somewhat better now': 2, 'About the same': 3,
                           'Somewhat worse now': 4, 'Much worse now': 5}
        mh_15_responses = {'Not at all': 1, 'Several days': 2, 'More than half the days': 3,
                           'Nearly every day': 4}
        mh_20_responses = {'Not at all stressful': 1, 'Not very stressful': 2, 'A bit stressful': 3,
                           'Quite a bit stressful': 4, 'Extremely stressful': 5}
        lm_30_responses = {'Strongly agree': 1, 'Agree': 2, 'Neither agree nor disagree': 3,
                           'Disagree': 4, 'Strongly disagree': 5,
                           'I have lost my job or business within the last 4 weeks': 6,
                           'Not working at a job or business': 7}
        # Note: we will be tracking the people in category 6 and 7 of LM_30_responses
        # above as unemployed

        age_responses = {'15 to 24 years old': 1, '25 to 34 years old': 2, '35 to 44 years old': 3,
                         '45 to 54 years old': 4, '55 to 64 years old': 5, '65 years and older': 6}
        with open(file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader)
            parsed_data = []
            for row in list(csv_reader):
                try:
                    mh_15_total = 0
                    for i in range(5, 12):
                        mh_15_total += mh_15_responses[row[i]]
                    mh_15_total = mh_15_total / 7
                    employment_status = False
                    if lm_30_responses[row[37]] <= 5:
                        employment_status = True

                    parsed_data.append({'mental health': (mh_5_responses[row[3]]
                                                          + mh_15_total + mh_20_responses[row[12]]),
                                        'employment': employment_status,
                                        'age': age_responses[row[32]],
                                        'mh_10': mh_10_responses[row[4]]})
                except KeyError:
                    # we ignore any data that hasn't been formatted correctly(for the first 80,
                    # there are 3 records not properly formatted)
                    continue

        self.all_data = parsed_data


def separate_on_employment(data: list[dict]) -> tuple[list[dict], list[dict]]:
    """
    Return separated data based on employment, from the given data, in tuple containing two
    list of dictionaries, corresponding to unemployed and employed respondents respectively

    >>> dataset = [{'age': 4, 'employment': False, 'mental health': 6.714285714285714, 'mh_10': 3}, \
    {'age': 3, 'employment': True, 'mental health': 4.0, 'mh_10': 3},\
    {'age': 3, 'employment': False, 'mental health': 7.428571428571429, 'mh_10': 4},\
    {'age': 4, 'employment': True, 'mental health': 8.571428571428571, 'mh_10': 4}]
    >>> sep = ([{'age': 4, 'employment': False, 'mental health': 6.714285714285714, 'mh_10': 3}, \
    {'age': 3, 'employment': False, 'mental health': 7.428571428571429, 'mh_10': 4}], \
    [{'age': 3, 'employment': True, 'mental health': 4.0, 'mh_10': 3},\
    {'age': 4, 'employment': True, 'mental health': 8.571428571428571, 'mh_10': 4}])
    >>> separate_on_employment(dataset) == sep
    True

    Preconditions:
     - all(type(person['employment']) == bool for person in data)
     - all(type(person['age']) == int for person in data)
     - all(type(person['mental health'] == float for person in data)

    """
    employed = []
    unemployed = []
    for person in data:
        if person['employment'] is False:
            unemployed.append(person)
        else:
            employed.append(person)
    return (unemployed, employed)


def separate_on_age_group(data: list[dict]) -> dict[int, list[dict]]:
    """
    Return data separated by age group, in form of dictionary with key corresponding to age group,
    and it's value as respondent data corresponding to that age group

    Preconditions:
     - all(type(person['employment']) == bool for person in data)
     - all(type(person['age']) == int for person in data)
     - all(type(person['mental health'] == float for person in data)

    >>> dataset = [{'age': 4, 'employment': False, 'mental health': 6.714285714285714, 'mh_10': 3},\
           {'age': 3, 'employment': True, 'mental health': 4.0, 'mh_10': 3},\
           {'age': 1, 'employment': True, 'mental health': 4.0, 'mh_10': 3},\
           {'age': 2, 'employment': False, 'mental health': 6.714285714285714, 'mh_10': 3},\
           {'age': 5, 'employment': True, 'mental health': 7.428571428571429, 'mh_10': 4},\
           {'age': 3, 'employment': False, 'mental health': 7.428571428571429, 'mh_10': 4},\
           {'age': 6, 'employment': True, 'mental health': 9.571428571428571, 'mh_10': 4},\
           {'age': 4, 'employment': True, 'mental health': 8.571428571428571, 'mh_10': 4}]
    >>> sep = {1: [{'age': 1, 'employment': True, 'mental health': 4.0, 'mh_10': 3}], \
    2: [{'age': 2, 'employment': False, 'mental health': 6.714285714285714, 'mh_10': 3}],\
    3: [{'age': 3, 'employment': True, 'mental health': 4.0, 'mh_10': 3}, \
    {'age': 3, 'employment': False, 'mental health': 7.428571428571429, 'mh_10': 4}],\
    4: [{'age': 4, 'employment': False, 'mental health': 6.714285714285714, 'mh_10': 3}, \
    {'age': 4, 'employment': True, 'mental health': 8.571428571428571, 'mh_10': 4}], \
    5: [{'age': 5, 'employment': True, 'mental health': 7.428571428571429, 'mh_10': 4}], \
    6: [{'age': 6, 'employment': True, 'mental health': 9.571428571428571, 'mh_10': 4}]}

    >>> sep == separate_on_age_group(dataset)
    True
    """
    separated = {}
    for i in range(1, 7):
        separated[i] = []
    for person in data:
        separated[person['age']].append(person)
    return separated


def avg_mental_health_ratio(data: list[dict]) -> float:
    """
    Return the average mental health ratio of all the people in the given data

    Preconditions:
     - all(type(person['employment']) == bool for person in data)
     - all(type(person['age']) == int for person in data)
     - all(type(person['mental health'] == float for person in data)

    >>> dataset = [{'age': 4, 'employment': False, 'mental health': 6.714285714285714, 'mh_10': 3},\
           {'age': 3, 'employment': True, 'mental health': 4.0, 'mh_10': 3},\
           {'age': 1, 'employment': True, 'mental health': 4.0, 'mh_10': 3},\
           {'age': 2, 'employment': False, 'mental health': 6.714285714285714, 'mh_10': 3},\
           {'age': 5, 'employment': True, 'mental health': 7.428571428571429, 'mh_10': 4},\
           {'age': 3, 'employment': False, 'mental health': 7.428571428571429, 'mh_10': 4},\
           {'age': 6, 'employment': True, 'mental health': 9.571428571428571, 'mh_10': 4},\
           {'age': 4, 'employment': True, 'mental health': 8.571428571428571, 'mh_10': 4}]
    >>> import math
    >>> math.isclose(avg_mental_health_ratio(dataset), 6.803571428571429)
    True
    """
    aggregate_mental_ratio = [person['mental health'] for person in data]
    return sum(aggregate_mental_ratio) / len(data)


def bar_graph_mental_health(data: list[dict]) -> None:
    """
    Plot the multiple bar graph, with x-axis separated between age groups, and the mental health
     ratio as y - axis

    Preconditions:
     - all(type(person['employment']) == bool for person in data)
     - all(type(person['age']) == int for person in data)
     - all(type(person['mental health'] == float for person in data)
    """
    age_responses = {'15 to 24 years old': 1, '25 to 34 years old': 2, '35 to 44 years old': 3,
                     '45 to 54 years old': 4, '55 to 64 years old': 5, '65 years and older': 6}
    age_sep1 = separate_on_age_group(data)
    index = age_responses.keys()
    employment_sep = {key: separate_on_employment(age_sep1[key]) for key in age_sep1}
    avg_mental_health = {i: [avg_mental_health_ratio(employment_sep[i][0]),
                             avg_mental_health_ratio(employment_sep[i][1])] for i in range(1, 7)}
    data_frame = pandas.DataFrame(avg_mental_health.values(),
                                  columns=['employed', 'unemployed'],
                                  index=index)
    data_frame.plot(y=["employed", "unemployed"], kind='bar', figsize=(8, 8), ylim=(0, 14),
                    title='Mental Health Ratio - Employment and Age Group')
    plt.show()


def count_on_mh10(data: list[dict]) -> dict[int, int]:
    """Return the number of people that responded with each of the option to MH_10:
    "Compared to before physical distancing began, how would you say your mental health is now?"
    as a dictionary with keys corresponding to response and value as corresponding count of people
    Preconditions:
     - all(type(person['employment']) == bool for person in data)
     - all(type(person['age']) == int for person in data)
     - all(type(person['mental health'] == float for person in data)

    >>> dataset = [{'age': 4, 'employment': False, 'mental health': 6.714285714285714, 'mh_10': 3},\
           {'age': 3, 'employment': True, 'mental health': 4.0, 'mh_10': 1},\
           {'age': 1, 'employment': True, 'mental health': 4.0, 'mh_10': 3},\
           {'age': 2, 'employment': False, 'mental health': 6.714285714285714, 'mh_10': 3},\
           {'age': 5, 'employment': True, 'mental health': 7.428571428571429, 'mh_10': 5},\
           {'age': 3, 'employment': False, 'mental health': 7.428571428571429, 'mh_10': 2},\
           {'age': 6, 'employment': True, 'mental health': 9.571428571428571, 'mh_10': 4},\
           {'age': 4, 'employment': True, 'mental health': 8.571428571428571, 'mh_10': 4}]
    >>> sep = {1: 1, 2: 1, 3: 3, 4: 2, 5: 1}
    >>> count_on_mh10(dataset) == sep
    True
    """
    mh_10_responses = {'Much better now': 1, 'Somewhat better now': 2, 'About the same': 3,
                       'Somewhat worse now': 4, 'Much worse now': 5}
    count = {}
    for i in mh_10_responses.values():
        count[i] = 0
    for person in data:
        count[person['mh_10']] += 1
    return count


def pie_chart_mental_effect(data: list[dict]) -> None:
    """Plot the pie chart, which shows the responses and their percentages for the question:
    "Compared to before physical distancing began, how would you say your mental health is now?"

    Preconditions:
     - all(type(person['employment']) == bool for person in data)
     - all(type(person['age']) == int for person in data)
     - all(type(person['mental health'] == float for person in data)
    """
    mh_10_responses = {'Much better now': 1, 'Somewhat better now': 2, 'About the same': 3,
                       'Somewhat worse now': 4, 'Much worse now': 5}
    count = count_on_mh10(data)
    index = mh_10_responses.keys()
    df = pandas.DataFrame([[i] for i in count.values()], index=index, columns=['MH_10'])
    df.plot(kind='pie', y='MH_10',
            title='Perceived Mental Health Change - post distancing measures', autopct='%1.1f%%')


# python_ta.check_all(config={
#     'extra-imports': ['csv', 'matplotlib.pyplot', 'pandas'],  # the names (strs) of imported modules
#     'allowed-io': ['load_data'],  # the names (strs) of functions that call print/open/input
#     'max-line-length': 100,
#     'disable': ['R1705', 'C0200']
# })
