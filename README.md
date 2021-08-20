# la_decarb_funding_analysis

## Project overview

This project aims to analyse and visualise the English local authorities receiving household decarbonisation grants from two different funding programmes: the [Green Homes Grant Local Authority Delivery scheme (GHG LADS)](https://www.gov.uk/government/publications/green-homes-grant-local-authority-delivery-successful-local-authorities) and the [Social Housing Decarbonisation Fund Demonstrator (SHDDF)](https://www.gov.uk/government/publications/social-housing-decarbonisation-fund-demonstrator-successful-bids). Local authority statistics are visualised alongside data about the number of grants they received, with the aim of identifying whether there are relationships between these different factors.

The GHG LADS was given out in two stages (1a and 1b) to different types of applicant (individual LAs and consortia of multiple LAs, consisting of a consortium lead and several members). The SHDDF was only given to individual LAs.

Several datasets are combined to form one large dataset with a row for each local authority. LA statistics consist of

- majority political party
- LA type (e.g. county, district, etc.)
- fuel poverty rate
- IMD local concentration
- median domestic energy efficiency rating
- number of EPCs corresponding to "improvable" social housing, i.e. socially rented homes that are currently EPC D or below and have the potential to be C or above
- grants received

The output of the project is a series of plots to feed into a report, which can be found [here](https://docs.google.com/document/d/1_X0-EWCxSwjH-ALmC_dlo3mm5i5Ieg4aH443y1Xb1yM/edit?usp=sharing).

## Project structure

- getters
  - local_authority_data_py
    - Functions to import individual datasets from inputs/data (stored in AWS).
- utils
  - name_cleaners.py
    - Utility functions to clean local authority names and types.
- pipeline
  - cleaning.py
    - Functions to clean the imported datasets.
  - joining.py
    - Functions to join all of the individual datasets into one larger dataset.
  - jitter_functions.py
    - Custom plotting functions.
  - plotters.py
    - Where the bulk of the plotting code lives.
- analysis
  - generate_plots.py
    - Runs the plotting functions and saves the results in outputs/figures.

## Setup

- Meet the data science cookiecutter [requirements](http://nestauk.github.io/ds-cookiecutter/quickstart), in brief:
  - Install: `git-crypt` and `conda`
  - Have a Nesta AWS account configured with `awscli`
- Run `make install` to configure the development environment:
  - Setup the conda environment
  - Configure pre-commit
  - Configure metaflow to use AWS

## Contributor guidelines

[Technical and working style guidelines](https://github.com/nestauk/ds-cookiecutter/blob/master/GUIDELINES.md)

---

<small><p>Project based on <a target="_blank" href="https://github.com/nestauk/ds-cookiecutter">Nesta's data science project template</a>
(<a href="http://nestauk.github.io/ds-cookiecutter">Read the docs here</a>).
</small>
