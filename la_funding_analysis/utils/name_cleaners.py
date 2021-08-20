# File: utils/name_cleaners.py
"""Functions to clean local authority names and model codes
in order to join data from difference sources
and make plots more readable.
"""

import numpy as np
import pandas as pd
from titlecase import titlecase


def clean_names(name) -> str:
    """Function to clean local authority names in various datasets
    in order to join data from different sources.
    """
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
    #
    replacements_dict = {
        "&": "and",
        "Mid-": "Mid ",
        "Upon": "upon",
        "Kings Lynn": "King's Lynn",
        "King’s Lynn": "King's Lynn",
        "Basingstoke and Deane": "Basingstoke and Dean",
        "St Helens": "St. Helens",
        "Vale of Whitehorse": "Vale of White Horse",
        "Newcastle upon Tyne": "Newcastle",
    }
    #
    for key, value in replacements_dict.items():
        name = name.replace(key, value)
    #
    name = name.strip()
    #
    return name


def strip_and_titlecase(name):
    """Function removing trailing spaces and making strings titlecase,
    used for cleaning region name data
    """
    if name is np.nan:
        return np.nan
    else:
        return titlecase(name.strip())


def model_type(code):
    """Function taking local authority model codes
    and returning a description of the model.
    """
    model_dict = {
        "U": "Unitary",
        "C": "County",
        "D": "District",
        "M": "Metropolitan borough",
        "L": "London borough",
        "S": "Scottish",
        "W": "Welsh",
        "N": "Northern Irish",
    }
    if pd.isna(code):
        full_type = np.nan
    else:
        full_type = model_dict[code[0]]
    return full_type
