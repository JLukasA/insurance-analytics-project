# Project description

Smaller insurance project case inspired by a case I came in contact with during an interview process. In this project I synthesise data and perform some basic data analysis using Python. 


## data_synthesis.py

With this file, the aforementioned data synthesis is done. Generates insurance claims data for vehicles (cars in this case). The synthesised liable claims data follows a Gamma distribution. Values are randomly generated separately for each year, seed set for replicability.

The following things are adjustable:
  _ Years to generate data for
  _ Number of insured vehicles to generate data for
  _ Yearly inflation rate
  _ Rate of claims (number of claims per insured vehicle per year)
  _ Liability ratio (percentage of non-zero valued claims to generate)
  _ Liable claims distribution

The generated data is written to an Excel-file, where the first sheet contains a table summarizing number of insured vehicles, number of claims and total cost of claims for each year. The second sheet contains individual claims data for all years.

## main.py 

This file contains the analysis performed using Python. Plots are generated, distributions are estimated and probabilities of certain events are calculated using this Python file. It is used more like a notebook.

## case_solution.pdf

Quickly translated and adjusted case solution, containing the stated problem and my solution.

## requirements.txt

libraries needed to run data_synthesis.py and main.py


