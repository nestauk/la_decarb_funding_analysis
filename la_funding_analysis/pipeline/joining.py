# File: pipeline/joining.py
"""Functions combining the data required for the analysis.
Datasets are added one at a time.
"""

from la_funding_analysis.pipeline.cleaning import (
    get_clean_fuel_poverty,
    get_clean_old_parties,
    get_clean_parties_models,
    get_clean_imd,
    get_clean_grants,
    get_clean_epc,
)


def custom_merge(data_1, data_2, on):
    """Customised merge function for joining all data.
    All merges will be left joins; also contains 1:1 validation for error checking
    """
    merged_data = data_1.merge(data_2, how="left", on=on)
    return merged_data


def form_fp_parties_models():
    """Forms a DataFrame from fuel poverty data (which also includes
    local authority structure) and majority party / LA model data.
    """
    fuel_poverty = get_clean_fuel_poverty()
    parties_models = get_clean_parties_models()
    old_parties = get_clean_old_parties()
    #
    fp_new_parties = custom_merge(fuel_poverty, parties_models, on="clean_name")
    fp_parties = custom_merge(fp_new_parties, old_parties, on="clean_name")
    #
    return fp_parties


def form_fp_pm_imd():
    """Forms a DataFrame combining fuel poverty, party/model
    and IMD proportion data.
    """
    fp_parties = form_fp_parties_models()
    imd = get_clean_imd()
    #
    fp_parties_imd = custom_merge(fp_parties, imd, on="clean_name")
    #
    return fp_parties_imd


def form_fp_pm_imd_grants():
    """Forms a DataFrame combining fuel poverty, party/model,
    IMD proportion and whether or not each local
    authority received a SHDF or GHG grant.
    """
    fp_parties_imd = form_fp_pm_imd()
    grants = get_clean_grants()
    # Missing data corresponds to 0 grants, so fill NAs in these cols with 0
    fp_parties_imd_grants = custom_merge(
        fp_parties_imd, grants, on="clean_name"
    ).fillna(
        {
            "GHG_1a_individuals": 0,
            "GHG_1a_leads": 0,
            "GHG_1a_bodies": 0,
            "GHG_1b_individuals": 0,
            "GHG_1b_leads": 0,
            "GHG_1b_bodies": 0,
            "SHDDF": 0,
            "total_grants": 0,
        }
    )
    return fp_parties_imd_grants


def form_all_data():
    """Forms a DataFrame combining fuel poverty, party/model,
    IMD, grants, median EPC data and improvable counts.
    """
    fp_parties_imd_grants = form_fp_pm_imd_grants()
    epc = get_clean_epc()
    #
    all_data = custom_merge(fp_parties_imd_grants, epc, on="code")
    #
    # Add column for local authorities that have high numbers of improvable homes
    # but did not receive SHDF grants - this will be used for plotting
    all_data["high_improvable_no_SHDDF"] = (all_data["SHDDF"] == 0) & (
        all_data["total_improvable"] > 20000
    )
    #
    return all_data


def form_all_tidy_data():
    """Forms a DataFrame combining all relevant data for the analysis
    in a tidy form for easier plotting.
    """
    all_data = form_all_data()
    #
    # Tidy up data types in preparation for plotting
    all_data = all_data.convert_dtypes()
    all_data["total_households"] = all_data["total_households"].astype("float")
    #
    # Add total cols for GHG 1a and 1b - useful for splitting by grant type
    all_data["total_grants_1a"] = (
        all_data["GHG_1a_individuals"]
        + all_data["GHG_1a_leads"]
        + all_data["GHG_1a_bodies"]
    )
    all_data["total_grants_1b"] = (
        all_data["GHG_1b_individuals"]
        + all_data["GHG_1b_leads"]
        + all_data["GHG_1b_bodies"]
    )
    all_data["1a_no_members"] = (
        all_data["GHG_1a_individuals"] + all_data["GHG_1a_leads"]
    )
    all_data["1b_no_members"] = (
        all_data["GHG_1b_individuals"] + all_data["GHG_1b_leads"]
    )
    all_data["all_no_members"] = (
        all_data["1a_no_members"] + all_data["1b_no_members"] + all_data["SHDDF"]
    )
    #
    all_tidy_data = all_data.reset_index(drop=True)
    #
    return all_tidy_data


#### Why are there 339 rows in this dataset when there are 333 LAs in England?
# This data is from last year when the grants were awarded;
# since then Northamptonshire CC and the 7 DCs below it
# have been replaced with two UCs
