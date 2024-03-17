"""
Largely inspired by the code provided in the Seaborn
documentation for Pairgrid Dotplots with multiple variables.

Seaborn Link: https://seaborn.pydata.org/examples/pairgrid_dotplot.html
Copyright 2012-2024 Michael Watson
"""

import seaborn as sns
from pandas import read_csv
import matplotlib.pyplot as plt

def make_graph():
    sns.set_theme(style="whitegrid")

    dataframe = read_csv("ratings.csv")
    #print(dataframe)

    albums = sns.PairGrid(dataframe,
                        x_vars=dataframe.columns[:-1],
                        y_vars=["Track_#"],
                        height=6,
                        aspect=.2)

    albums.map(sns.stripplot, size=8, orient="h",
            jitter=False, linewidth=1, edgecolor="w")

    albums.set(xlim=(0,50), ylabel="")


    for ax in albums.axes.flat:
        ax.xaxis.grid(False)
        ax.yaxis.grid(True)

    #sns.despine(left=True, bottom=True)
    plt.savefig("seaborn_plot.jpg", dpi=300)

if __name__=="__main__":
    make_graph()