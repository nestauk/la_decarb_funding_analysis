# File: utils/plotters.py
"""Functions to assist with plotting.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def rand_jitter(arr):
    # Function to add small variation to values in a list.
    stdev = 0.01 * (max(arr) - min(arr))
    return arr + np.random.randn(len(arr)) * stdev


def jitter(
    x,
    y,
    s=20,
    c="b",
    marker="o",
    cmap=None,
    norm=None,
    vmin=None,
    vmax=None,
    alpha=None,
    linewidths=None,
    verts=None,
    hold=None,
    **kwargs
):
    # Function to make a jitter plot, with jitter only in the x direction.
    return plt.scatter(
        rand_jitter(x),
        y,
        s=s,
        c=c,
        marker=marker,
        cmap=cmap,
        norm=norm,
        vmin=vmin,
        vmax=vmax,
        alpha=alpha,
        linewidths=linewidths,
        **kwargs
    )


def strip_plot(data, value, ymin, ymax, graph_ylabel, graph_title, filename):
    # Function to make a 'strip plot'
    # (a scatter plot with one discrete axis)
    # with number of grants on the x axis
    # and a specified value on the y axis.
    # Includes some jitter in the x direction.
    plt.clf()
    data_notna = data[~data[value].isna()]
    plot = jitter(
        x=data_notna["total_grants"],
        y=data_notna[value],
        s=data_notna["total_households"] / 10000,
        alpha=0.4,
    )
    plt.axis([-0.5, 4.5, ymin, ymax])
    plt.xlabel("Number of grants")
    plt.ylabel(graph_ylabel)
    plt.title(graph_title)
    kw = dict(prop="sizes", num=5, func=lambda s: 10000 * s)
    plt.legend(*plot.legend_elements(**kw), title="Total households")
    plt.savefig(filename)
    plt.close()


def proportion_plot(data, category, graph_ylabel, graph_title, filename):
    # Function to plot a bar graph in which bars are
    # scaled to the number of LAs in the chosen category.
    # Bars are coloured according to the number of LAs
    # receiving each number of grants.
    num_grants = (
        data.groupby([category, "total_grants"])
        .size()
        .reset_index(name="counts")
        .pivot(index=category, columns="total_grants", values="counts")
        .fillna(0)
    )
    num_grants["total"] = num_grants.sum(axis=1)
    prop_grants = pd.DataFrame()
    for i in [0, 1, 2, 3, 4]:
        prop_grants[i] = num_grants[i] / num_grants["total"]
    prop_grants = prop_grants.reset_index().sort_values([0, 1, 2, 3, 4])
    my_cmap = plt.get_cmap("viridis")
    prop_grants.plot(
        x=category,
        kind="barh",
        stacked=True,
        color=my_cmap([1, 0.75, 0.5, 0.25, 0]),
        title=graph_title,
        zorder=2,
    )
    plt.xlim([-0, 1])
    plt.xlabel("Proportion of local authorities")
    plt.ylabel(graph_ylabel)
    plt.legend(loc="center left", bbox_to_anchor=(1, 0.5))
    plt.grid(axis="x", zorder=0)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()


def stacked_plot(data, factor, graph_ylabel, graph_title, filename):
    # Function to make a stacked bar chart in which
    # sections are coloured according to the number of
    # grants of each type.
    subtotals = (
        data[["total_grants_1a", "total_grants_1b", "SHDF", factor, "total_grants"]]
        .groupby(factor)
        .sum()
        .sort_values("total_grants")
        .drop(columns="total_grants")
        .rename(columns={"total_grants_1a": "GHG 1a", "total_grants_1b": "GHG 1b"})
    )
    my_cmap = plt.get_cmap("tab10")
    subtotals.plot.barh(stacked=True, color=my_cmap([1, 2, 3]), zorder=2)
    plt.ylabel(graph_ylabel)
    plt.xlabel("Number of grants")
    plt.grid(axis="x", zorder=0)
    plt.title(graph_title)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
