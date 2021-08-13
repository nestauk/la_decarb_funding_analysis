# File: analysis/generate_plots.py
"""Produces plots and stores them in /outputs/figures.
"""

from la_funding_analysis.pipeline.joining import form_all_tidy_data
from la_funding_analysis.pipeline.plotters import (
    imd_strip_plot,
    improvable_strip_plot,
    proportion_by_number_of_grants,
    stacked_no_members_by_grant_type,
    dual_bar_by_applicant_type,
    boxplot_by_receipt_status,
    fp_clusters_strip_plot,
    westmids_london_fp_strip_plot,
)

la_data = form_all_tidy_data()

# STACKED BAR CHARTS

stacked_no_members_by_grant_type(
    data=la_data,
    factor="region_1",
    graph_ylabel="Number of grants",
    graph_title="Number of grants by region for each funding scheme\n(individual authorities and consortium leads only)",
    filename="final_stack_region.svg",
)

stacked_no_members_by_grant_type(
    data=la_data,
    factor="model",
    graph_ylabel="Number of grants",
    graph_title="Number of grants by local authority type\nfor each funding scheme\n(individual authorities and consortium leads only)",
    filename="final_stack_model.svg",
)

# PROPORTION PLOTS

proportion_by_number_of_grants(
    data=la_data,
    factor="region_1",
    graph_ylabel="Region (Total LAs)",
    graph_title="Percentages of local authorities in each region\nreceiving each number of grants\n(including consortium members)",
    filename="final_prop_region.svg",
)

proportion_by_number_of_grants(
    data=la_data,
    factor="majority",
    graph_ylabel="Majority party (Total LAs)",
    graph_title="Percentages of local authorities receiving grants,\nby political composition and number of grants received",
    filename="final_prop_majority.svg",
)

# DUAL BAR CHART

dual_bar_by_applicant_type(
    data=la_data,
    factor="model",
    graph_ylabel="Type",
    graph_title="Percentages of local authorities participating\nin GHG LAD and SHDDF by type",
    filename="final_dual_type.svg",
)

# BOXPLOT

boxplot_by_receipt_status(
    data=la_data,
    factor="median_energy_efficiency",
    graph_ylabel="Median household energy efficiency",
    graph_title="Median household energy efficiency in each local authority\nvs whether or not they received a grant",
    filename="final_boxplot_median.svg",
)


# STRIP PLOTS

# IMD

imd_strip_plot(data=la_data, filename="final_strip_imd.svg")

# FP, coloured clusters

fp_clusters_strip_plot(data=la_data, filename="final_strip_fp.svg")

# FP by region

westmids_london_fp_strip_plot(data=la_data, filename="final_strip_fp_regions.svg")


# Improvable vs SHDF

improvable_strip_plot(
    data=la_data, factor="total_improvable", filename="final_strip_improvable_count.svg"
)

improvable_strip_plot(
    data=la_data, factor="prop_improvable", filename="final_strip_improvable_prop.svg"
)
