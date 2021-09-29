from la_funding_analysis.pipeline.cleaning_and_joining import (
    get_clean_parties_models,
    form_england_fp_parties_models,
    get_clean_fuel_poverty,
    get_clean_grants,
    form_all_tidy_data,
)

la_data = form_all_tidy_data()

# Why is Northampton appearing twice in la_data?

pm = get_clean_parties_models()
pm.loc[pm.name.str.contains("Northampton")]
# Northampton appears once

fp = get_clean_fuel_poverty()
fp.loc[fp.region_3 == "Northampton"]
# Northampton appears once

fp_parties = form_england_fp_parties_models()
fp_parties.loc[fp_parties.region_3 == "Northampton"]
# Northampton appears twice, with two different models


names_to_codes = fp.set_index("clean_name")["code"]
pm["code"] = pm["code"].fillna(names_to_codes)
pm = pm.set_index("code").drop(columns="name")
fp_parties = fp.join(pm, on="code", how="left")


filtered = la_data[
    [
        "code",
        "region_1",
        "region_2",
        "region_3",
        "GHG_1a_LADS",
        "GHG_1a_leads",
        "GHG_1a_bodies",
        "GHG_1b_LADS",
        "GHG_1b_leads",
        "GHG_1b_bodies",
        "SHDF",
    ]
]
filtered_eng = filtered[filtered.region_1 != "Scotland"]
filtered_eng["total_grants"] = (
    filtered_eng.GHG_1a_LADS
    + filtered_eng.GHG_1a_leads
    + filtered_eng.GHG_1a_bodies
    + filtered_eng.GHG_1b_LADS
    + filtered_eng.GHG_1b_leads
    + filtered_eng.GHG_1b_bodies
    + filtered_eng.SHDF
)

filtered_eng["total_relevant_grants"] = (
    filtered_eng.GHG_1a_LADS
    + filtered_eng.GHG_1a_leads
    + filtered_eng.GHG_1b_LADS
    + filtered_eng.GHG_1b_leads
    + filtered_eng.SHDF
)
filtered_eng["is_relevant"] = filtered_eng.total_relevant_grants >= 1

individual_or_lead = filtered_eng[filtered_eng.is_relevant]

filtered_eng["body_grants"] = filtered_eng.GHG_1a_bodies + filtered_eng.GHG_1b_bodies

the_rest = filtered_eng.loc[~filtered_eng.is_relevant & filtered_eng.body_grants >= 1]


grants = get_clean_grants()
missing_names = [
    name for name in grants.index if name not in [name2 for name2 in fp.clean_name]
]
la_data.loc[[("Babergh" in name) for name in la_data.clean_name]]
la_data.loc[[("Mid Suffolk" in name) for name in la_data.clean_name]]


la_data_lowest_regions[
    [("(Met County)" in thing) for thing in la_data_lowest_regions.region_2]
]
la_data[[("(Met County)" in thing) for thing in la_data.region_2]]


la_data[list(la_data.model.isna())]

met = list(la_data.region_2.str.contains("(Met County)"))
no3 = list(la_data.region_3.isna())
both = [a and b for a, b in zip(met, no3)]
info_sp = la_data.drop(la_data[both].index)


num_grants = (
    la_data.groupby(["majority", "total_grants"])
    .size()
    .reset_index(name="counts")
    .pivot(index="majority", columns="total_grants", values="counts")
    .fillna(0)
)
num_grants["total"] = num_grants.sum(axis=1)
prop_grants = pd.DataFrame()
for i in [4, 3, 2, 1]:
    prop_grants[i] = num_grants[i] / num_grants["total"]


num_grants = (
    la_data.groupby(["majority", "total_grants"])
    .size()
    .reset_index(name="counts")
    .pivot(index="majority", columns="total_grants", values="counts")
    .fillna(0)
)
num_grants["total"] = num_grants.sum(axis=1)
prop_grants = pd.DataFrame()
for i in [4, 3, 2, 1]:
    prop_grants[i] = num_grants[i] / num_grants["total"]
prop_grants = prop_grants.loc[
    (prop_grants[4] + prop_grants[3] + prop_grants[2] + prop_grants[1])
    .sort_values()
    .index
]


len(la_data[la_data.model == "County"][["region_2", "region_3", "total_grants"]])


subtotals = (
    la_data[["1a_no_members", "1b_no_members", "SHDF", "model", "all_no_members"]]
    .groupby("model")
    .sum()
    .sort_values("all_no_members")
    .drop(columns="all_no_members")
    .rename(
        columns={
            "1a_no_members": "GHG LAD 1a",
            "1b_no_members": "GHG LAD 1b",
            "SHDF": "SHDDF",
        }
    )
)


data_notna = la_data[~la_data["fp_proportion"].isna()]
tl_cond1 = data_notna["total_grants"] == 0
tl_cond2 = data_notna["fp_proportion"] > 20
tl_conds = [a and b for a, b in zip(tl_cond1, tl_cond2)]
top_left = data_notna[tl_conds]


# individuals
len(la_data[la_data["GHG_1a_LADS"] + la_data["GHG_1b_LADS"] + la_data["SHDF"] >= 2])
la_data[la_data["GHG_1a_LADS"] + la_data["GHG_1b_LADS"] + la_data["SHDF"] >= 2]

# individuals and leads
len(la_data[la_data["all_no_members"] == 3])

# totals
len(la_data[la_data["total_grants"] == 4])

# leads
len(la_data[la_data["GHG_1a_leads"] + la_data["GHG_1b_leads"] == 3])
