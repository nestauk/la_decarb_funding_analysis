# File: getters/local_authority_data.py
"""Functions to import all data.
"""

import pandas as pd


def get_fuel_poverty():
    fuel_poverty = pd.read_excel(
        "https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/981910/2021-sub-regional-fuel-poverty-tables.xlsx",
        sheet_name="Table 2",
        skiprows=2,
        skipfooter=7,
    ).rename(
        columns={
            "Area Codes": "code",
            "Area name": "region_1",
            "Unnamed: 2": "region_2",
            "Unnamed: 3": "region_3",
            "Number of households1": "total_households",
            "Number of households in fuel poverty1": "fp_households",
            "Proportion of households fuel poor (%)": "fp_proportion",
        }
    )
    return fuel_poverty


def get_parties_models():
    parties_models = pd.read_csv(
        "http://opencouncildata.co.uk/csv1.php", usecols=[1, 2, 5, 24]
    ).rename(
        columns={
            "model (C=county, D=district, 1=all-up, 3=thirds, etc.)": "model",
            "ons code": "code",
        }
    )
    return parties_models


def get_imd():
    # Source: http://www.gov.uk/government/statistics/english-indices-of-deprivation-2019
    imd = pd.read_csv(
        "inputs/data/societal-wellbeing_imd2019_indicesbyla.csv",
        usecols=[1, 2],
        skiprows=7,
    )
    return imd


def get_grants():
    # Sources:
    # http://www.gov.uk/government/publications/green-homes-grant-local-authority-delivery-successful-local-authorities
    # http://www.gov.uk/government/publications/social-housing-decarbonisation-fund-demonstrator-successful-bids
    grants = pd.read_excel(
        "inputs/data/Local_authorities_and_decarbonisation_schemes.xlsx",
        dtype={"Local authority": str},
        skiprows=[1],
        usecols="A:I",
    ).fillna(0)
    return grants


def get_EPC_means():
    # Source: Processed version of EPC data obtained from
    # http://www.github.com/nestauk/EPC_data_analysis
    EPC_means = (
        pd.read_csv("inputs/data/EPC_means.csv")
        .rename(
            columns={
                "LOCAL_AUTHORITY": "code",
                "CURRENT_ENERGY_EFFICIENCY": "mean_energy_efficiency",
            }
        )
        .set_index("code")
    )
    return EPC_means


def get_social_potential():
    # Source: Processed version of EPC data obtained from
    # http://www.github.com/nestauk/EPC_data_analysis
    social_potential = pd.read_csv("inputs/data/social_epc_potential.csv").drop(
        columns="Unnamed: 0"
    )
    return social_potential
