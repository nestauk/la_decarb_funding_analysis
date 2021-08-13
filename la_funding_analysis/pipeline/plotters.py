# File: utils/plotters.py
"""Functions to assist with plotting.
"""
from la_funding_analysis import PROJECT_DIR
from la_funding_analysis.utils.jitter_functions import jitter

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick


# STACKED HORIZONTAL BAR PLOTS


def stacked_no_members_by_grant_type(data, factor, graph_ylabel, graph_title, filename):
    """Function to make a stacked bar chart of grants awarded to
    individual LAs and consortium leads (no members) split by factor
    in which sections are coloured according to the number of
    grants of each type.
    """
    subtotals = (
        data[["1a_no_members", "1b_no_members", "SHDDF", factor, "all_no_members"]]
        .groupby(factor)
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
    fig, ax = plt.subplots()
    my_cmap = plt.get_cmap("tab10")
    subtotals.plot.barh(stacked=True, color=my_cmap([1, 2, 3]), zorder=2)
    plt.ylabel(graph_ylabel)
    plt.xlabel("Number of grants")
    plt.grid(axis="x", zorder=0)
    plt.title(graph_title)
    plt.tight_layout()
    plt.savefig(PROJECT_DIR / "outputs/figures" / filename)


# PROPORTION HORIZONTAL BAR PLOTS


def proportion_by_number_of_grants(data, factor, graph_ylabel, graph_title, filename):
    # Function to plot a bar graph in which bars are
    # scaled to the number of LAs in the chosen factor.
    # Bars are coloured according to the number of LAs
    # receiving each number of grants.
    data = data[~data[factor].isna()]
    la_counts = data.groupby(factor).count()["code"]
    num_factors = len(set(data[factor]))
    #
    new_index = [
        (la_counts.index[i] + " (" + str(la_counts.values[i]) + ")")
        for i in range(0, num_factors)
    ]
    num_grants = (
        data.groupby([factor, "total_grants"])
        .size()
        .reset_index(name="counts")
        .pivot(index=factor, columns="total_grants", values="counts")
        .fillna(0)
    )
    num_grants["total"] = num_grants.sum(axis=1)
    prop_grants = pd.DataFrame()
    for i in [4, 3, 2, 1, 0]:
        prop_grants[i] = num_grants[i] / num_grants["total"]
    prop_grants["new_index"] = new_index
    prop_grants = prop_grants.set_index("new_index")
    prop_grants = prop_grants.reset_index().sort_values(0, ascending=False)
    #
    fig, ax = plt.subplots()
    my_cmap = plt.get_cmap("viridis")
    ax = prop_grants.plot(
        x="new_index",
        kind="barh",
        stacked=True,
        color=my_cmap([0, 0.25, 0.5, 0.75, 1]),
        title=graph_title,
        zorder=2,
    )
    plt.xlim([0, 1])
    ax.xaxis.set_major_formatter(
        mtick.PercentFormatter(xmax=1, decimals=None, symbol="%", is_latex=False)
    )
    plt.xlabel("Percentage of local authorities")
    plt.ylabel(graph_ylabel)
    plt.legend(title="Number of grants", loc="center left", bbox_to_anchor=(1, 0.5))
    plt.grid(axis="x", zorder=0)
    plt.tight_layout()
    plt.savefig(PROJECT_DIR / "outputs/figures" / filename)


# DUAL BAR CHART


def dual_bar_by_applicant_type(data, factor, graph_ylabel, graph_title, filename):
    """Classifies LAs in each factor by whether or not they received a grant
    and whether or not they were an individual / consortium lead,
    then plots the frequency in each factor.
    """
    data["grant"] = data["total_grants"] >= 1
    data["ind_lead"] = data["all_no_members"] >= 1
    types = data[[factor, "grant", "ind_lead"]].groupby("model").agg(["sum", "count"])
    types["Individual or consortium lead only"] = (
        types["ind_lead"]["sum"] / types["grant"]["count"]
    )
    types["Individual/lead/consortium member"] = (
        types["grant"]["sum"] / types["grant"]["count"]
    )
    types.columns = types.columns.droplevel(1)
    types = types.drop(columns=["grant", "ind_lead"])
    #
    ax = types.plot(kind="barh", zorder=2)
    ax.xaxis.set_major_formatter(
        mtick.PercentFormatter(xmax=1, decimals=None, symbol="%", is_latex=False)
    )
    plt.title(graph_title)
    plt.xlim([0, 1])
    ax.set_xticks(np.linspace(0, 1, 11))
    plt.legend(
        reversed(plt.legend().legendHandles),
        [
            "Individuals, leads and consortium members",
            "Individuals and consortium leads only",
        ],
        bbox_to_anchor=(0.5, -0.4),
        loc="lower center",
    )
    plt.grid(axis="x", zorder=0)
    plt.ylabel(graph_ylabel)
    plt.xlabel("Percentage of local authorities")
    plt.tight_layout()
    plt.savefig(PROJECT_DIR / "outputs/figures" / filename)
    plt.close()


# BOXPLOT


def boxplot_by_receipt_status(data, factor, graph_ylabel, graph_title, filename):
    data["received_grant"] = data["total_grants"] >= 1
    data["Received at least one grant"] = "No"
    data["Received at least one grant"][data["received_grant"]] = "Yes"
    fig, ax = plt.subplots()
    data.boxplot(factor, by="Received at least one grant")
    # plt.ylim([45,75])
    plt.suptitle("")
    plt.title(graph_title)
    plt.ylabel(graph_ylabel)
    plt.grid(False)
    plt.savefig(PROJECT_DIR / "outputs/figures" / filename)


# STRIP PLOTS


def set_up_strip_plot_axes(axes, ymin, ymax, graph_ylabel, graph_title, type="ngrants"):
    axes.grid(axis="y", color="#d3d3d3", zorder=0)
    if type == "ngrants":
        xmin = -0.5
        xmax = 4.5
        graph_xlabel = "Number of grants"
    if type == "yesno":
        xmin = -0.4
        xmax = 1.4
        graph_xlabel = "Received SHDDF"
        axes.set_xticks([0, 1])
        axes.set_xticklabels(["No", "Yes"])
    axes.set_axisbelow(True)
    axes.set_xlim([xmin, xmax])
    axes.set_ylim([ymin, ymax])
    axes.set_xlabel(graph_xlabel)
    axes.set_ylabel(graph_ylabel)
    axes.set_title(graph_title)
    return axes


def imd_strip_plot(data, filename):
    fig, ax = plt.subplots()
    set_up_strip_plot_axes(
        axes=ax,
        ymin=10000,
        ymax=35000,
        graph_ylabel="IMD local concentration",
        graph_title="IMD local concentration of local authorities\nvs number of grants obtained",
        type="ngrants",
    )
    data_notna = data[~data["imd_concentration"].isna()]
    jitter(
        axes=ax,
        x=data_notna["total_grants"],
        y=data_notna["imd_concentration"],
        alpha=0.25,
        zorder=5,
    )
    plt.savefig(PROJECT_DIR / "outputs/figures" / filename)


def fp_clusters_strip_plot(data, filename):
    data_notna = data[~data["fp_proportion"].isna()]
    #
    tl_cond1 = data_notna["total_grants"] == 0
    tl_cond2 = data_notna["fp_proportion"] > 20
    tl_conds = [a and b for a, b in zip(tl_cond1, tl_cond2)]
    top_left = data_notna[tl_conds]
    #
    mr_cond1 = data_notna["total_grants"] == 3
    mr_cond2 = data_notna["fp_proportion"] < 15
    mr_conds = [a and b for a, b in zip(mr_cond1, mr_cond2)]
    middle_right = data_notna[mr_conds]
    #
    tl_index = top_left.index
    mr_index = middle_right.index
    rest = data_notna.drop(tl_index).drop(mr_index)
    #
    fig, ax = plt.subplots()
    #
    set_up_strip_plot_axes(
        axes=ax,
        ymin=0,
        ymax=25,
        graph_ylabel="Fuel poor households (%)",
        graph_title="Fuel poverty rate of local authorities\nvs number of grants obtained",
        type="ngrants",
    )
    plot_list = [
        (top_left, {"c": "red", "alpha": 0.4, "zorder": 6}),
        (middle_right, {"c": "green", "alpha": 0.4, "zorder": 5}),
        (rest, {"c": "blue", "alpha": 0.25, "zorder": 2}),
    ]
    for df, plot_args in plot_list:
        jitter(axes=ax, x=df["total_grants"], y=df["fp_proportion"], **plot_args)
    plt.savefig(PROJECT_DIR / "outputs/figures" / filename)


def westmids_london_fp_strip_plot(data, filename):
    data_notna = data[~data["fp_proportion"].isna()]
    #
    wm_data = data_notna[data_notna["region_1"] == "West Midlands"]
    london_data = data_notna[data_notna["region_1"] == "London"]
    neither_data = data_notna.drop(wm_data.index).drop(london_data.index)
    fig, ax = plt.subplots()
    set_up_strip_plot_axes(
        axes=ax,
        ymin=0,
        ymax=25,
        graph_ylabel="Fuel poor households (%)",
        graph_title="Fuel poverty rate of local authorities\nvs number of grants obtained",
        type="ngrants",
    )
    plot_list = [
        (wm_data, {"c": "red", "alpha": 0.35, "zorder": 6}),
        (london_data, {"c": "blue", "alpha": 0.35, "zorder": 5}),
        (neither_data, {"c": "grey", "alpha": 0.25, "zorder": 2}),
    ]
    for df, plot_args in plot_list:
        jitter(axes=ax, x=df["total_grants"], y=df["fp_proportion"], **plot_args)
    ax.legend(["West Midlands", "London", "Other"], title="Region", loc="lower right")
    plt.savefig(PROJECT_DIR / "outputs/figures" / filename)


# Improvable social housing plots


def improvable_strip_plot(data, factor, filename):
    # Count/prop of socially rented homes that are improvable vs SHDF yes/no
    data_notna = data[~data[factor].isna()]
    fig, ax = plt.subplots()
    #
    if factor == "total_improvable":
        ymin = 0
        ymax = 40000
        graph_ylabel = "Number of EPCs for improvable socially rented dwellings"
        graph_title = "Number of EPCs for improvable socially rented dwellings\nvs whether or not the local authority received a SHDDF grant"
    if factor == "prop_improvable":
        ymin = 0
        ymax = 0.7
        graph_ylabel = "Percentage of registered EPCs for\nsocially rented dwellings that are improvable"
        graph_title = "Percentage of registered EPCs for socially rented dwellings\nthat are improvable vs whether or not\nthe local authority received a SHDDF grant"
        ax.set_xticks([0, 1])
        ax.set_xticklabels(["No", "Yes"])
        ax.yaxis.set_major_formatter(
            mtick.PercentFormatter(xmax=1, decimals=None, symbol="%", is_latex=False)
        )
    #
    set_up_strip_plot_axes(
        axes=ax,
        ymin=ymin,
        ymax=ymax,
        graph_ylabel=graph_ylabel,
        graph_title=graph_title,
        type="yesno",
    )
    standout_points = data_notna[data_notna["high_improvable_no_SHDDF"]].reset_index(
        drop=True
    )
    other_points = data_notna[~data_notna["high_improvable_no_SHDDF"]]
    plot_list = [
        (standout_points, {"c": "red", "alpha": 0.5, "deviation": 0, "zorder": 6}),
        (other_points, {"c": "blue", "alpha": 0.1, "deviation": 0.01, "zorder": 1}),
    ]
    for df, plot_args in plot_list:
        jitter(axes=ax, x=df["SHDDF"], y=df[factor], **plot_args)
    #
    ax.annotate(
        "County Durham",
        (0.02, standout_points[factor][0]),
        fontsize=8,
    )
    ax.annotate(
        standout_points["region_3"][1],
        (0.02, standout_points[factor][1]),
        fontsize=8,
    )
    ax.annotate(
        standout_points["region_3"][2],
        (0.02, standout_points[factor][2]),
        fontsize=8,
    )
    plt.tight_layout()
    plt.savefig(PROJECT_DIR / "outputs/figures" / filename)
