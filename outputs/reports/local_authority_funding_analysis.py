# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     comment_magics: true
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.11.3
#   kernelspec:
#     display_name: la_funding_analysis
#     language: python
#     name: la_funding_analysis
# ---

# %% [markdown]
# # Local authority funding analysis
#
# ## Summary and aims
#
# The aim of this analysis was to identify which types of local authority were most successful in obtaining grants from two different government funding programmes, the Green Homes Grant (GHG) and the Social Housing Decarbonisation Fund (SHDF), with the broader aim of identifying whether the funding went to the local authorities that needed it most.
#
# The GHG is being awarded to both individual local authorities and consortia in England in two phases (1a and 1b). The programme is intended to fund energy efficiency and low carbon heating projects for low income households, thereby reducing fuel poverty.
#
# The SHDF was awarded to local authorities in England and Scotland to fund projects retrofitting social housing at scale, aiming to bring homes up to EPC C or higher.
#
# The mechanism of delivering funding via local authorities is likely to be used more in the future, so it is important that local authorities have the capacity to engage with funding schemes.
#
# ## Data and limitations
#
# Data on which local authorities received funding was collected from gov.uk. These were combined with data on the local authorities’ higher-tier regions, structure and political composition, along with data on their rates of fuel poverty, indices of multiple deprivation (IMD) and domestic energy efficiency.
#
# Some limitations of the data were as follows:
# * Grants could be given to any ‘level’ of local authority; it was not possible to identify which lower-tier regions received funding as a result of their higher-tier region receiving a grant
# * The sizes of GHG grants was unknown, and in particular it was unknown whether grants to consortia were the same size as grants to individual local authorities, or whether they were proportional to the number of bodies in the consortium
# * The distribution of funding within a successful consortium was unknown
# * Data about which local authorities actually applied for funding was not available

# %% [markdown]
# ## Profile of successful local authorities
#
# ### Local authority regions
#
# Consortium bodies have been excluded from these plots in order to better represent the number of grants going to each region.

# %% [markdown]
# ![region_plot_by_grant.png](attachment:region_plot_by_grant.png)

# %% [markdown]
# Local authorities in the South East appear to be less successful in receiving SHDF grants, although this may be due to underlying factors such as low levels of socially rented housing in these areas, and relatively few SHDF grants were distributed.

# %% [markdown]
# ![region_props.png](attachment:region_props.png)

# %% [markdown]
# Areas in London appear to be more successful in receiving grants than other regions.

# %% [markdown]
# ### Local authority models

# %% [markdown]
# ![model_plot_by_grant.png](attachment:model_plot_by_grant.png)

# %% [markdown]
# ![model_props.png](attachment:model_props.png)

# %% [markdown]
# Again we see a high number of grants given to London boroughs compared to other types of local authority.

# %% [markdown]
# ### Political composition

# %% [markdown]
# ![party_plot_by_grant.png](attachment:party_plot_by_grant.png)

# %% [markdown]
# ![party_props.png](attachment:party_props.png)

# %% [markdown]
# Labour and Liberal Democrat majority areas appear to be more successful in obtaining grants, though this may be due to underlying factors such as high fuel poverty and energy inefficiency associated with these areas. Independent majority areas appear to be less successful, although there are only 9 of these areas in total.

# %% [markdown]
# ## Is the money following the need?
#
# In the plots below, only local authorities without subregions have been considered to avoid double-counting. Only English local authorities have been considered due to data limitations, and since different measures are used in England and Scotland.
#
# ### Fuel poverty

# %% [markdown]
# ![fp_plot.png](attachment:fp_plot.png)

# %% [markdown]
# There appears to be some correlation between the number of grants received by a local authority and its proportion of fuel poor households. The local authority receiving 4 grants was the London Borough of Barking and Dagenham, which has the highest proportion of fuel poor households in England.
#
# The top-left cluster of points on the graph consists of local authorities that received no grants but have comparatively high rates of fuel poverty. All of these local authorities are in the West Midlands:

# %% [markdown]
# Region | Unitary or county council | District or borough council | Total households | Fuel poor households (%) | Total grants
# -----|-----|-----|-----|-----|-----
# West Midlands | Stoke-on-Trent | | 115172 | 21.823 | 0
# West Midlands | West Midlands (Met County) | Birmingham | 439526 | 21.157 | 0
# West Midlands | West Midlands (Met County) | Wolverhampton | 109199 | 21.128 | 0
# West Midlands | West Midlands (Met County) | Sandwell | 129918 | 20.949 | 0

# %% [markdown]
# The middle-right cluster of points on the graph consists of local authorities that received three grants but have comparatively low rates of fuel poverty. The majority of these local authorities are in the South West or London:

# %% [markdown]
# Region | Unitary or county council | District or borough council | Total households | Fuel poor households (%) | Total grants
# -----|-----|-----|-----|-----|-----
# South West | Gloucestershire | Stroud | 52539 | 10.164 | 3
# London | Outer London | Richmond upon Thames | 85182 | 10.606 | 3
# South East | East Sussex | Hastings | 44311 | 10.787 | 3
# South West | Somerset  | Sedgemoor | 53755 | 10.818 | 3
# South West | Devon | West Devon | 25010 | 11.483 | 3
# South West | Devon | Exeter | 54298 | 11.859 | 3
# London | Inner London | Kensington and Chelsea | 84022 | 12.864 | 3
# London | Inner London | Wandsworth | 139052 | 13.152 | 3
# East | Suffolk | West Suffolk | 76831 | 13.659 | 3

# %% [markdown]
# The plot below is equivalent to the one above, but with points coloured according to their region:

# %% [markdown]
# ![fp_westmids_london.png](attachment:fp_westmids_london.png)

# %% [markdown]
# There are some signs here that authorities in the West Midlands are missing out - authorities in London have similar rates of fuel poverty but have received more grants.

# %% [markdown]
# ### IMD

# %% [markdown]
# ![imd_plot.png](attachment:imd_plot.png)

# %% [markdown]
# There appears to be some correlation between the number of grants received by a local authority and its IMD concentration.

# %% [markdown]
# ### EPC

# %% [markdown]
# ![epc_plot.png](attachment:epc_plot.png)

# %% [markdown]
# There does not appear to be a strong correlation between the number of grants received by a local authority and the mean energy efficiency of its households.
#
# The stated aim of the SHDF was to bring energy inefficient social housing up to EPC C or higher. The plot below shows the number of socially rented dwellings in each local authority which are currently EPC D or below and have the potential to be EPC C or above, against whether or not the local authority received a grant from the SHDF:

# %% [markdown]
# ![improvable_counts.png](attachment:improvable_counts.png)

# %% [markdown]
# A small cluster of points can be seen in the top left, corresponding to local authorities with many improvable socially rented dwellings that did not receive SHDF funding. These are all metropolitan areas in the midlands or northeast of England. Many of the local authorities receiving SHDF grants do not appear to be ones with a comparatively high number of improvable socially rented dwellings.
#
# Plotting against the proportion of improvable socially rented dwellings instead of the absolute number, we see that the local authorities receiving SHDF funding are not ones with particularly high proportions. The points in the cluster from the plot above have been highlighted.

# %% [markdown]
# ![improvable_props.png](attachment:improvable_props.png)

# %% [markdown]
# ## Conclusions and future research
#
# While the funding does seem to be following the need to some extent, there are several areas in the midlands and the north of England with high rates of fuel poverty and/or energy inefficiency that did not receive funding from this round of grants.
#
# Some areas for future investigation are as follows:
# * In the plots above, local authorities were only deemed to have received funding if they had received it directly, but it is possible that they would also receive funding indirectly if their upper-tier local authority received funding, so it would be worth replicating the analysis under this assumption.
# * It would be good to find out and utilise the amounts of funding given to each local authority. This data is available for the SHDF, but not for the GHG.
# * It would also be useful to find out which local authorities applied to these grants and were unsuccessful, as opposed to local authorities that did not apply.
# * If the areas highlighted above applied and were unsuccessful then it would be good to understand why - do the socially rented dwellings in these areas have certain properties that make them difficult to retrofit?
