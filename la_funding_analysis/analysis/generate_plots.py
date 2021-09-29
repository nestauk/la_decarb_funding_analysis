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


def produce_charts(suffix):
    """Produces all charts for the analysis with the given suffix (e.g. .png)"""
    # STACKED BAR CHARTS
    #
    stacked_no_members_by_grant_type(
        data=la_data,
        factor="region_1",
        graph_ylabel="Number of grants",
        graph_title="Number of grants by region for each funding scheme\n(individual authorities and consortium leads only)",
        filename="final_stack_region" + suffix,
    )
    #
    stacked_no_members_by_grant_type(
        data=la_data,
        factor="model",
        graph_ylabel="Number of grants",
        graph_title="Number of grants by local authority type\nfor each funding scheme\n(individual authorities and consortium leads only)",
        filename="final_stack_model" + suffix,
    )
    #
    # PROPORTION PLOTS
    #
    proportion_by_number_of_grants(
        data=la_data,
        factor="region_1",
        graph_ylabel="Region (Total LAs)",
        graph_title="Percentages of local authorities in each region\nreceiving each number of grants\n(including consortium members)",
        filename="final_prop_region" + suffix,
    )
    #
    proportion_by_number_of_grants(
        data=la_data,
        factor="majority",
        graph_ylabel="Majority party (Total LAs)",
        graph_title="Percentages of local authorities receiving grants,\nby political composition in August 2021\nand number of grants received",
        filename="final_prop_majority" + suffix,
    )
    #
    proportion_by_number_of_grants(
        data=la_data,
        factor="old_majority",
        graph_ylabel="Majority party (Total LAs)",
        graph_title="Percentages of local authorities receiving grants,\nby political composition in August 2020\nand number of grants received",
        filename="final_prop_old_majority" + suffix,
    )
    #
    # DUAL BAR CHART
    dual_bar_by_applicant_type(
        data=la_data,
        factor="model",
        graph_ylabel="Type",
        graph_title="Percentages of local authorities participating\nin GHG LAD and SHDDF by type",
        filename="final_dual_type" + suffix,
    )
    #
    # BOXPLOT
    boxplot_by_receipt_status(
        data=la_data,
        factor="median_energy_efficiency",
        graph_ylabel="Median energy efficiency of registered EPCs",
        graph_title="Median energy efficiency of registered EPCs\nin each local authority vs whether or not they received a grant",
        filename="final_boxplot_median" + suffix,
    )
    #
    #
    # STRIP PLOTS
    #
    # IMD
    imd_strip_plot(data=la_data, filename="final_strip_imd" + suffix)
    #
    # FP, coloured clusters
    fp_clusters_strip_plot(data=la_data, filename="final_strip_fp" + suffix)
    #
    # FP by region
    westmids_london_fp_strip_plot(
        data=la_data, filename="final_strip_fp_regions" + suffix
    )
    #
    # Number of improvable vs SHDDF
    improvable_strip_plot(
        data=la_data,
        factor="total_improvable",
        filename="final_strip_improvable_count" + suffix,
    )
    #
    # Proportion of improvable vs SHDDF
    improvable_strip_plot(
        data=la_data,
        factor="prop_improvable",
        filename="final_strip_improvable_prop" + suffix,
    )


produce_charts(suffix=".png")
produce_charts(suffix=".svg")
