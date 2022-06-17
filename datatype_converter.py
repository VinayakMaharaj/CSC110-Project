"""CSC110 Fall 2021 Project Phase 2: Datatype Convertor

File Instructions
===============================
This file contains a small line of code that can be used to convert file types from dta to csv

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of TA's and professors
working at CSC110 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are...
not really minded. Please do credit though!

This file is Copyright (c) 2021 Madhav Kanna Thenappan, Prahlad Ranjit, Amirali Tolooei,
and Vinayak Maharaj.
"""
import pandas as pd


def conversion(file: str) -> None:
    """Converts from dta to csv when a directory is entered in the format: r'datafile.dta' and
    creates a new file in the format of csv on the same directory it is within (the file)"""
    data = pd.io.stata.read_stata(file)
    data.to_csv('my_stata_file.csv')
