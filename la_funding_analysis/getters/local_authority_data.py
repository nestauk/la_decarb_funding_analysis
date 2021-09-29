# File: getters/local_authority_data.py
"""Functions to import all data.
"""

import pandas as pd

from la_funding_analysis import PROJECT_DIR


def get_fuel_poverty():
    """Fetches fuel poverty data. Also contains information about LA regional structure.
    Source: https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/981910/2021-sub-regional-fuel-poverty-tables.xlsx
    """
    fuel_poverty = pd.read_excel(
        PROJECT_DIR / "inputs/data/2021-sub-regional-fuel-poverty-tables.xlsx",
        sheet_name="Table 2",
        skiprows=2,
        skipfooter=7,
    )
    return fuel_poverty


def get_parties_models():
    """Fetches data about LA model types (i.e. county, district etc.)
    and majority political parties as of August 2021.
    Source: http://opencouncildata.co.uk/csv1.php
    """
    parties_models = pd.read_csv(
        PROJECT_DIR / "inputs/data/opencouncildata_councils.csv", usecols=[1, 2, 5]
    )
    return parties_models


def get_old_parties():
    """Fetches data about LA majority parties as of 2019.
    Source: http://opencouncildata.co.uk/downloads.php
    """
    old_parties = pd.read_csv(
        PROJECT_DIR / "inputs/data/history1973-2019.csv", usecols=[0, 3, 10]
    )
    #
    old_parties = old_parties.loc[old_parties["Year"] == 2019].drop(columns="Year")
    #
    return old_parties


def get_imd():
    """Fetches data about LA IMD status.
    The "local concentration" measure is used -
    this gives higher weight to particularly deprived areas
    Source: http://www.gov.uk/government/statistics/english-indices-of-deprivation-2019
    """
    imd = pd.read_csv(
        PROJECT_DIR / "inputs/data/societal-wellbeing_imd2019_indicesbyla.csv",
        usecols=[1, 2],
        skiprows=7,
    )
    return imd


def get_grants():
    """Fetches data on which LAs received GHG and SHDF grants.
    Sources:
    http://www.gov.uk/government/publications/green-homes-grant-local-authority-delivery-successful-local-authorities
    http://www.gov.uk/government/publications/social-housing-decarbonisation-fund-demonstrator-successful-bids
    """
    grants = pd.read_excel(
        PROJECT_DIR / "inputs/data/Local_authorities_and_decarbonisation_schemes.xlsx",
        dtype={"Local authority": str},
        skiprows=[1],
        usecols="A:I",
    ).fillna(0)
    #
    return grants


def get_epc():
    """Fetches English LA EPC data. Quite big so takes a few seconds."""
    epc = pd.read_csv(PROJECT_DIR / "inputs/data/epc.csv").drop(columns="Unnamed: 0")
    #
    return epc
