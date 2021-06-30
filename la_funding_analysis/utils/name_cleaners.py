# File: utils/name_cleaners.py
"""Functions to clean local authority names and model codes
in order to join data from difference sources
and make plots more readable.
"""

import numpy as np
import pandas as pd


def clean_names(name) -> str:
    # Function to clean local authority names in various datasets
    # in order to join data from different sources.
    strings = [
        " Metropolitan Borough Council",
        " Metropolitan District Council",
        " Royal Borough Council",
        "Royal Borough of ",
        "London Borough of ",
        " Borough Council",
        " District Council",
        " City Council",
        " County Council",
        "District",
        "Council",
        "Corporation",
        ", City of",
        "City of ",
        ", County of",
        "County UA",
        "County ",
        " (Met County)",
        "CC",
        "DC",
    ]
    name = name.replace("\xa0", " ")
    for string in strings:
        name = name.replace(string, "")
    name = (
        name.replace("&", "and")
        .replace("Mid-", "Mid ")
        .replace("Upon", "upon")
        .replace("Kings Lynn", "King's Lynn")
        .replace("King’s Lynn", "King's Lynn")
        .replace("Basingstoke and Deane", "Basingstoke and Dean")
        .replace("St Helens", "St. Helens")
        .replace("Vale of Whitehorse", "Vale of White Horse")
        .replace("Newcastle upon Tyne", "Newcastle")
        .strip()
    )
    return name


def model_type(code):
    # Function taking local authority model codes
    # and returning a description of the model.
    model_dict = {
        "U": "Unitary",
        "C": "County",
        "D": "District",
        "M": "Metropolitan",
        "L": "London",
        "S": "Scottish",
        "W": "Welsh",
        "N": "Northern Irish",
    }
    if pd.isna(code):
        full_type = np.nan
    else:
        full_type = model_dict[code[0]]
    return full_type


# print(model_type('L3'))
