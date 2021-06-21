# File: pipeline/cleaning_and_joining.py
"""Cleans and joins the imported datasets to form
a dataframe info_sp containing all information about
local authorities and the grants they received.
"""

import numpy as np
import pandas as pd
from titlecase import titlecase

from la_funding_analysis.getters.local_authority_data import (
    get_EPC_means,
    get_grants,
    get_imd,
    get_parties_models,
    get_fuel_poverty,
    get_social_potential,
)
from la_funding_analysis.utils.name_cleaners import clean_names, model_type


# First import fuel poverty data - this also includes data on
# how the local authorities are structured in England, so we
# can join IMD, party, EPC and grants data onto it
fuel_poverty = get_fuel_poverty()

# Merge the different region columns into one and apply clean_names
fuel_poverty["clean_name"] = (
    fuel_poverty["region_1"]
    .fillna(fuel_poverty["region_2"])
    .fillna(fuel_poverty["region_3"])
    .apply(clean_names)
)

names_to_codes = fuel_poverty.set_index("clean_name")["code"]

# Import LA majority parties and models; this also contains Scottish data
parties_models = get_parties_models()

# All Scottish regions have model S1 - extract these to append later
scottish_regions = parties_models[parties_models["model"] == "S1"]

# Apply clean_names to all names in parties/models data
parties_models["clean_name"] = parties_models["name"].apply(clean_names)
parties_models = parties_models.set_index("clean_name")

parties_models["code"] = parties_models["code"].fillna(names_to_codes)
parties_models = parties_models.set_index("code").drop(columns="name")

# Join fuel poverty / region hierarchy data to parties/models
fp_parties = fuel_poverty.join(parties_models, on="code")

# Fill in NaN values in geographic columns:
# first copy region_1 values into region_2 then forward-fill region_2 -
# the region_1s stop the filling from going too far
fp_parties["region_2"] = fp_parties["region_2"].fillna(fp_parties["region_1"]).ffill()
# Set the copied-over values in region_2 back to NaN
fp_parties["region_2"].loc[~fp_parties["region_1"].isna()] = np.nan
# Then forward-fill region_1
fp_parties["region_1"] = fp_parties["region_1"].ffill()

# Append Scottish data
scottish_regions = scottish_regions.rename(columns={"name": "region_2"})
scottish_regions["clean_name"] = scottish_regions["region_2"].apply(clean_names)
scottish_regions["region_1"] = "SCOTLAND"
fp_parties = fp_parties.append(scottish_regions)

# It will be useful later to have a column indicating whether a region
# is one that contains subregions
# The 'region_2' value of a row is a region with subregions
# if there is more than one row with this region_2 value
# in the table, so group by these and sum
totals = (
    fp_parties.groupby(["region_1", "region_2"])
    .size()
    .reset_index(name="counts")
    .assign(r2_subregions=lambda x: (x.counts > 1))
    .set_index("region_2")
    .drop(columns=["region_1", "counts"])
)

fp_parties_tot = fp_parties.join(totals, on="region_2")

# A region has subregions if it is a region_1
# or if its region_2 has subregions and it is not a region_3
fp_parties_tot["r1_row"] = fp_parties_tot["region_2"].isna()
fp_parties_tot["r3_row"] = ~fp_parties_tot["region_3"].isna()
fp_parties_tot["subregions"] = fp_parties_tot["r1_row"] | (
    fp_parties_tot["r2_subregions"] & ~fp_parties_tot["r3_row"]
)

fp_parties_sub = fp_parties_tot.drop(columns=["r2_subregions", "r1_row", "r3_row"])


# Add IMD data
imd = get_imd()

imd["clean_name"] = imd["Reference area"].apply(clean_names)
imd = imd.set_index("clean_name")

fp_parties_imd = (
    fp_parties_sub.join(imd, on="clean_name")
    .drop(columns="Reference area")
    .rename(columns={" Local concentration": "imd_concentration"})
)

# Check: missing clean names?
# set(fp_parties_sub['clean_name']).difference(set(imd.index))

# Now join onto grants by clean_name
grants = get_grants()

# Some regions appear twice in the grants data
duplicate_strings = ["Greenwich", "Lewisham", "Redbridge"]
regex_exp = "|".join(duplicate_strings)
clean_grants = grants[~grants["Local authority"].str.contains(regex_exp, regex=True)]

for string in duplicate_strings:
    duplicate_df = grants[grants["Local authority"].str.contains(string)]
    replacement_row = duplicate_df.iloc[0] + duplicate_df.iloc[1]
    replacement_row["Local authority"] = string
    clean_grants = clean_grants.append(replacement_row, ignore_index=True)

# As before, apply clean_names in order to join data
clean_grants["Clean LA name"] = clean_grants["Local authority"].apply(clean_names)
clean_grants = clean_grants.set_index("Clean LA name")

fp_parties_imd_grants = fp_parties_imd.join(clean_grants, on="clean_name").drop(
    columns="Local authority"
)

# Rename columns so they are easier to use
fp_parties_imd_grants = fp_parties_imd_grants.rename(
    columns={
        "GHG LADS 1a": "GHG_1a_LADS",
        "1a Consortium Leads": "GHG_1a_leads",
        "1a Consortium bodies": "GHG_1a_bodies",
        "GHG LADS 1b": "GHG_1b_LADS",
        "1b Consortium leads": "GHG_1b_leads",
        "1b Consortium bodies": "GHG_1b_bodies",
        "Social Housing Decarbonisation Fund - Demonstrator ": "SHDF",
        "Total": "total_grants",
    }
)

# Missing data corresponds to 0 grants, so fill NAs in these cols with 0
fp_parties_imd_grants = fp_parties_imd_grants.fillna(
    {
        "GHG_1a_LADS": 0,
        "GHG_1a_leads": 0,
        "GHG_1a_bodies": 0,
        "GHG_1b_LADS": 0,
        "GHG_1b_leads": 0,
        "GHG_1b_bodies": 0,
        "SHDF": 0,
        "total_grants": 0,
    }
)

# Filter out all of the region_1 rows (could do this sooner)
fp_parties_imd_grants = fp_parties_imd_grants[~fp_parties_imd_grants["region_2"].isna()]


# Append EPC means
EPC_means = get_EPC_means()

info_grants = fp_parties_imd_grants.join(EPC_means, on="code")


# Tidy up data types in preparation for plotting
info_grants = info_grants.convert_dtypes()
info_grants["total_households"] = info_grants["total_households"].astype("float")

# Rename 'model' column to make it more readable in plots
info_grants["model"] = info_grants["model"].apply(model_type)

# Add total cols for GHG 1a and 1b - useful for splitting by grant type
info_grants["total_grants_1a"] = (
    info_grants["GHG_1a_LADS"]
    + info_grants["GHG_1a_leads"]
    + info_grants["GHG_1a_bodies"]
)
info_grants["total_grants_1b"] = (
    info_grants["GHG_1b_LADS"]
    + info_grants["GHG_1b_leads"]
    + info_grants["GHG_1b_bodies"]
)

# Clean region_1 column
info_grants["region_1"] = info_grants["region_1"].apply(lambda x: titlecase(x.strip()))


# Append counts/proportions of potentially improvable social housing
social_potential = get_social_potential()

sp_counts = (
    social_potential.groupby(["LOCAL_AUTHORITY", "potential"])[
        ["LOCAL_AUTHORITY", "potential"]
    ]
    .size()
    .reset_index()
)

# Reshape dataframe
sp_counts = sp_counts.pivot(index="LOCAL_AUTHORITY", columns="potential", values=0)

sp_counts["total_social"] = sp_counts.sum(axis=1)
sp_counts = sp_counts.rename(columns={True: "improvable", False: "not_improvable"})

# Calculate proportions
sp_counts["prop_improvable"] = sp_counts["improvable"] / sp_counts["total_social"]
sp_counts["prop_not_improvable"] = (
    sp_counts["not_improvable"] / sp_counts["total_social"]
)

info_sp = info_grants.join(sp_counts, on="code")

# print(info_sp.head())
