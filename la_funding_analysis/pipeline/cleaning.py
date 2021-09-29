# File: pipeline/cleaning.py
"""Functions to clean datasets.
Calling each function returns a clean version of the associated dataset.
"""

import numpy as np
import pandas as pd

from la_funding_analysis.getters.local_authority_data import (
    get_epc,
    get_grants,
    get_imd,
    get_old_parties,
    get_parties_models,
    get_fuel_poverty,
)
from la_funding_analysis.utils.name_cleaners import (
    clean_names,
    model_type,
    strip_and_titlecase,
)


def get_clean_fuel_poverty():
    """Gets and cleans fuel poverty dataset."""
    fuel_poverty = get_fuel_poverty()
    #
    fuel_poverty = fuel_poverty.rename(
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
    #
    # Remove trailing spaces and fix capitalisation in region columns
    fuel_poverty["region_1"] = fuel_poverty["region_1"].apply(strip_and_titlecase)
    fuel_poverty["region_2"] = fuel_poverty["region_2"].apply(strip_and_titlecase)
    fuel_poverty["region_3"] = fuel_poverty["region_3"].apply(strip_and_titlecase)
    #
    # Merge the different 'region' columns into one and apply clean_names -
    # this allows for joining onto data in which local authorities
    # are only referred to by name and not ID
    fuel_poverty["clean_name"] = (
        fuel_poverty["region_1"]
        .fillna(fuel_poverty["region_2"])
        .fillna(fuel_poverty["region_3"])
        .apply(clean_names)
    )
    # Fill in NaN values in region columns so that all region_3 rows
    # have associated region_1 and region_2 data,
    # and all region_2 rows have associated region_1 data.
    # First copy region_1 values into region_2 then forward-fill region_2 -
    # the 'region_1's stop the filling from going too far
    fuel_poverty["region_2"] = (
        fuel_poverty["region_2"].fillna(fuel_poverty["region_1"]).ffill()
    )
    # Set the copied-over values in region_2 back to NaN
    fuel_poverty["region_2"].loc[~fuel_poverty["region_1"].isna()] = np.nan
    # Then forward-fill region_1
    fuel_poverty["region_1"] = fuel_poverty["region_1"].ffill()
    # Filter out all of the region_1 rows - they are not local authorities
    fuel_poverty = fuel_poverty[~fuel_poverty["region_2"].isna()]
    # Additionally remove all Met Counties and Inner/Outer London -
    # these are rows that contain (Met County) or Inner/Outer London in region_2
    # and have NA region_3
    def not_la_condition(string):
        return ("(Met County)" in string) | (string in ["Inner London", "Outer London"])

    #
    #
    not_las = [not_la_condition(string) for string in fuel_poverty["region_2"]]
    no_region_3 = list(fuel_poverty.region_3.isna())
    both = [a and b for a, b in zip(not_las, no_region_3)]
    fuel_poverty = fuel_poverty.drop(fuel_poverty[both].index)
    #
    # Append rows for Greater London Authority and
    # Greater Manchester Combined Authority -
    # these are not LAs but some grants went to them
    combined_authorities = pd.DataFrame(
        [
            [
                np.nan,
                "London",
                "Greater London Authority",
                np.nan,
                np.nan,
                np.nan,
                np.nan,
                "Greater London Authority",
            ],
            [
                np.nan,
                "North West",
                "Greater Manchester Combined Authority",
                np.nan,
                np.nan,
                np.nan,
                np.nan,
                "Greater Manchester Combined Authority",
            ],
        ],
        columns=fuel_poverty.columns,
    )
    #
    fuel_poverty = fuel_poverty.append(combined_authorities, ignore_index=True)
    #
    return fuel_poverty


def get_clean_parties_models():
    """Gets and cleans current LA majority party and model (e.g. county, district) data."""
    parties_models = get_parties_models()
    #
    parties_models = parties_models.rename(
        columns={
            "model (C=county, D=district, 1=all-up, 3=thirds, etc.)": "model",
        }
    )
    # 'Buckinghamshire' row in this dataset is incorrect -
    # it is labelled as a County council but it has become unitary
    # Manually replace with the correct data
    # Source: http://opencouncildata.co.uk/council.php?c=413&y=0
    parties_models.loc[2] = ["Buckinghamshire", "U1", "CON"]
    #
    # Rename models to full names
    parties_models["model"] = parties_models["model"].apply(model_type)
    #
    # Apply clean_names to all names in parties/models data
    parties_models["clean_name"] = parties_models["name"].apply(clean_names)
    parties_models = parties_models.drop(columns="name")
    #
    return parties_models


def get_clean_old_parties():
    """Gets and cleans data about political majorities as of August 2020."""
    op = get_old_parties()
    op["clean_name"] = op["Authority"].apply(clean_names)
    op["old_majority"] = [string.upper() for string in op["Control"]]
    op = op.drop(columns=["Authority", "Control"]).reset_index(drop=True)
    return op


def get_clean_imd():
    """Gets and cleans IMD data."""
    imd = get_imd()
    imd = imd.rename(
        columns={
            "Reference area": "full_name",
            " Local concentration": "imd_concentration",
        }
    )
    #
    imd["clean_name"] = imd["full_name"].apply(clean_names)
    imd = imd.drop(columns="full_name")
    #
    return imd


def get_clean_grants():
    """Gets and cleans data on grants received by LAs."""
    grants = get_grants()
    grants = grants.rename(
        columns={
            "Local authority": "full_name",
            "GHG LADS 1a": "GHG_1a_individuals",
            "1a Consortium Leads": "GHG_1a_leads",
            "1a Consortium bodies": "GHG_1a_bodies",
            "GHG LADS 1b": "GHG_1b_individuals",
            "1b Consortium leads": "GHG_1b_leads",
            "1b Consortium bodies": "GHG_1b_bodies",
            "Social Housing Decarbonisation Fund - Demonstrator ": "SHDDF",
            "Total": "total_grants",
        }
    )
    #
    # Some regions appear twice in the grants data
    duplicate_strings = ["Greenwich", "Lewisham", "Redbridge"]
    regex_exp = "|".join(duplicate_strings)
    clean_grants = grants[~grants["full_name"].str.contains(regex_exp, regex=True)]
    #
    for string in duplicate_strings:
        duplicate_df = grants[grants["full_name"].str.contains(string)]
        replacement_row = duplicate_df.iloc[0] + duplicate_df.iloc[1]
        replacement_row["full_name"] = string
        clean_grants = clean_grants.append(replacement_row, ignore_index=True)
    #
    # Babergh and Mid Suffolk are shown in one row in the grants data,
    # but they are actually two different LAs - the stated grants
    # apply to both individually
    babergh_ms = clean_grants[
        [("Babergh and Mid Suffolk" in name) for name in clean_grants["full_name"]]
    ]
    babergh = babergh_ms.copy()
    babergh["full_name"] = "Babergh"
    ms = babergh_ms.copy()
    ms["full_name"] = "Mid Suffolk"
    clean_grants = (
        clean_grants[
            [
                ("Babergh and Mid Suffolk" not in name)
                for name in clean_grants["full_name"]
            ]
        ]
        .append(babergh)
        .append(ms)
        .reset_index(drop=True)
    )
    #
    # As before, apply clean_names in order to join data
    clean_grants["clean_name"] = clean_grants["full_name"].apply(clean_names)
    clean_grants = clean_grants.drop(columns="full_name")
    #
    return clean_grants


def get_clean_epc():
    """Processes EPC dataset to obtain median EPC for each LA
    and counts/proportions of improvable social housing.
    """
    epc = get_epc()
    #
    # Calculate median energy rating for each LA:
    epc_medians = (
        epc.groupby("LOCAL_AUTHORITY")["CURRENT_ENERGY_EFFICIENCY"]
        .apply(np.median)
        .reset_index(name="median_energy_efficiency")
    )
    #
    # Calculate proportions of 'improvable' social housing
    # (socially rented dwellings that are currently EPC D or below,
    # and have the potential to be C or above)
    #
    # There are two different strings signifying socially rented
    # in the TENURE column of the EPC data:
    epc_social = epc.loc[epc["TENURE"].isin(["rental (social)", "Rented (social)"])]
    #
    epc_social["is_improvable"] = (
        epc_social["CURRENT_ENERGY_RATING"].isin(["G", "F", "E", "D"])
    ) & (epc_social["POTENTIAL_ENERGY_RATING"].isin(["C", "B", "A"]))
    #
    # Find the numbers of improvable / not improvable social houses in each LA
    potential_counts = (
        epc_social.groupby(["LOCAL_AUTHORITY", "is_improvable"])[
            ["LOCAL_AUTHORITY", "is_improvable"]
        ]
        .size()
        .reset_index(name="count")
        .pivot(index="LOCAL_AUTHORITY", columns="is_improvable", values="count")
        .rename(columns={True: "total_improvable", False: "total_not_improvable"})
    )
    # Calculate proportions
    potential_counts.columns.name = None
    potential_counts["total_social"] = potential_counts.sum(axis=1)
    potential_counts["prop_improvable"] = (
        potential_counts["total_improvable"] / potential_counts["total_social"]
    )
    potential_counts = potential_counts.reset_index()[
        ["LOCAL_AUTHORITY", "total_improvable", "prop_improvable"]
    ]
    # Join to medians
    clean_epc = epc_medians.merge(potential_counts, on="LOCAL_AUTHORITY").rename(
        columns={"LOCAL_AUTHORITY": "code"}
    )
    #
    return clean_epc
