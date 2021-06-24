# File: analysis/generate_plots.py
"""Produces plots and stores them in /outputs/figures.
"""

import matplotlib.pyplot as plt

from la_funding_analysis.pipeline.cleaning_and_joining import form_full_dataset
from la_funding_analysis.utils.plotters import (
    jitter,
    strip_plot,
    proportion_plot,
    stacked_plot,
)

la_data = form_full_dataset()

# Region proportions
proportion_plot(
    data=la_data,
    category="region_1",
    graph_ylabel="Region",
    graph_title="Proportions of local authorities in each region\n receiving each number of grants\n (individual authorities and consortium leads only)",
    filename="outputs/figures/region_props.png",
)

# Party proportions
proportion_plot(
    data=la_data,
    category="majority",
    graph_ylabel="Majority party",
    graph_title="Proportions of local authorities with each majority party\n receiving each number of grants",
    filename="outputs/figures/party_props.png",
)

# Model proportions
proportion_plot(
    data=la_data,
    category="model",
    graph_ylabel="Local authority model",
    graph_title="Proportions of local authorities with each model\n receiving each number of grants",
    filename="outputs/figures/model_props.png",
)

# Majority party plot by grant type
stacked_plot(
    data=la_data,
    factor="majority",
    graph_ylabel="Majority party",
    graph_title="Number of grants by majority party for each funding scheme",
    filename="outputs/figures/party_plot_by_grant.png",
)

# LA type by grant
stacked_plot(
    data=la_data,
    factor="model",
    graph_ylabel="Local authority model",
    graph_title="Number of grants by local authority model\n for each funding scheme",
    filename="outputs/figures/model_plot_by_grant.png",
)


# Filter to regions without subregions
la_data_lowest_regions = la_data[~la_data["subregions"]]

# Plot by region, ignoring consortium members
no_members = la_data_lowest_regions[
    ["region_1", "GHG_1a_LADS", "GHG_1a_leads", "GHG_1b_LADS", "GHG_1b_leads", "SHDF"]
]
no_members["GHG 1a"] = no_members["GHG_1a_LADS"] + no_members["GHG_1a_leads"]
no_members["GHG 1b"] = no_members["GHG_1b_LADS"] + no_members["GHG_1b_leads"]
no_members["total"] = no_members["GHG 1a"] + no_members["GHG 1b"] + no_members["SHDF"]
regions_totals = (
    no_members.groupby("region_1")
    .sum()
    .sort_values("total")
    .drop(
        columns=["GHG_1a_LADS", "GHG_1a_leads", "GHG_1b_LADS", "GHG_1b_leads", "total"]
    )
)
regions_totals = regions_totals[["GHG 1a", "GHG 1b", "SHDF"]]
my_cmap = plt.get_cmap("tab10")
regions_totals.plot.barh(stacked=True, color=my_cmap([1, 2, 3]), zorder=2)
plt.ylabel("Region")
plt.xlabel("Number of grants")
plt.xticks(range(0, 30, 5))
plt.title(
    "Number of grants by region for each funding scheme\n (individual authorities and consortium leads only)"
)
plt.grid(axis="x", zorder=0)
plt.tight_layout()
plt.savefig("outputs/figures/region_plot_by_grant.png")
plt.close()


# FP plot
strip_plot(
    data=la_data_lowest_regions,
    value="fp_proportion",
    ymin=0,
    ymax=25,
    graph_ylabel="Fuel poor households (%)",
    graph_title="Average fuel poverty of local authorities vs number of grants obtained\n (authorities without subregions only)",
    filename="outputs/figures/fp_plot.png",
)

# Fuel poverty proportion vs SHDF yes/no, West Mids and London shown
la_data_lr_filtered = la_data_lowest_regions[
    ~la_data_lowest_regions["fp_proportion"].isna()
]
west_mids = la_data_lr_filtered[la_data_lr_filtered["region_1"] == "West Midlands"]
london = la_data_lr_filtered[la_data_lr_filtered["region_1"] == "London"]
non_wm_lon = la_data_lr_filtered.drop(west_mids.index).drop(london.index)

plt.clf()
fig, ax = plt.subplots()
jitter(
    x=west_mids["total_grants"],
    y=west_mids["fp_proportion"],
    c="red",
    alpha=0.35,
    zorder=6,
)
jitter(
    x=london["total_grants"], y=london["fp_proportion"], c="blue", alpha=0.35, zorder=5
)
jitter(
    x=non_wm_lon["total_grants"],
    y=non_wm_lon["fp_proportion"],
    c="grey",
    alpha=0.25,
    zorder=2,
)
plt.axis([-0.5, 4.5, 0, 25])
plt.xlabel("Number of grants")
plt.ylabel("Fuel poor households (%)")
plt.grid(axis="y", color="#d3d3d3", zorder=0)
plt.title(
    "Average fuel poverty of local authorities vs number of grants obtained\n (authorities without subregions only, to avoid double-counting)"
)
plt.legend(["West Midlands", "London", "Other"], title="Region", loc="lower right")
plt.savefig("outputs/figures/fp_westmids_london.png")

# IMD plot
strip_plot(
    data=la_data_lowest_regions,
    value="imd_concentration",
    ymin=10000,
    ymax=35000,
    graph_ylabel="IMD concentration",
    graph_title="IMD concentration of local authorities vs number of grants obtained\n (authorities without subregions only)",
    filename="outputs/figures/imd_plot.png",
)

# EPC plot
strip_plot(
    data=la_data_lowest_regions,
    value="mean_energy_efficiency",
    ymin=54,
    ymax=70,
    graph_ylabel="Mean energy efficiency",
    graph_title="Mean energy efficiency vs number of grants obtained\n (authorities without subregions only)",
    filename="outputs/figures/epc_plot.png",
)


# Improvable social housing plots

# Filter to England only
la_data_eng = la_data[la_data["region_1"] != "Scotland"]

# Separate "high improvability, low grants" points
# so they can be shown in a different colour
big = la_data_eng[(la_data_eng["SHDF"] == 0) & (la_data_eng["improvable"] > 20000)]
small = la_data_eng.drop(big.index)
big = big.reset_index()

# Number of improvable socially rented homes vs SHDF yes/no
fig, ax = plt.subplots()
jitter(x=small["SHDF"], y=small["improvable"], alpha=0.2)
jitter(x=big["SHDF"], y=big["improvable"], alpha=0.5, c="red")
ax.set_ylabel("Number of improvable socially rented dwellings")
ax.set_ylim([0, 30000])
ax.set_xticks([0, 1])
ax.set_xlim([-0.4, 1.4])
ax.set_xlabel("Received SHDF")
ax.set_xticklabels(["No", "Yes"])
ax.annotate("County Durham", (0.02, big["improvable"][0]), fontsize=8)
ax.annotate(big["region_3"][1], (0.02, big["improvable"][1] - 500), fontsize=8)
ax.annotate(big["region_3"][2], (0.02, big["improvable"][2] - 1000), fontsize=8)
plt.title(
    "Number of improvable socially rented dwellings\n vs SHDF receipt status (English local authorities only)"
)
plt.savefig("outputs/figures/improvable_counts.png")

# Proportion of socially rented homes that are improvable vs SHDF yes/no
fig, ax = plt.subplots()
jitter(x=small["SHDF"], y=small["prop_improvable"], alpha=0.2)
jitter(x=big["SHDF"], y=big["prop_improvable"], alpha=0.5, c="red")
ax.set_ylabel("Proportion of socially rented dwellings that are improvable")
ax.set_ylim([0, 0.7])
ax.set_xticks([0, 1])
ax.set_xlim([-0.4, 1.4])
ax.set_xlabel("Received SHDF")
ax.set_xticklabels(["No", "Yes"])
ax.annotate("County Durham", (0.02, big["prop_improvable"][0]), fontsize=8)
ax.annotate(big["region_3"][1], (0.02, big["prop_improvable"][1]), fontsize=8)
ax.annotate(big["region_3"][2], (0.02, big["prop_improvable"][2]), fontsize=8)
plt.title(
    "Proportion of socially rented dwellings that are improvable\n vs SHDF receipt status (English local authorities only)"
)
plt.savefig("outputs/figures/improvable_props.png")
