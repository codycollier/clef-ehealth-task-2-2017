#!/usr/bin/env python
"""Create chart(s) for a topic run

"""

import os.path

import matplotlib.pyplot as plt


def chart(filename=None, out_directory=None):
    """Show or save a plot"""
    if filename and out_directory:
        outpath = os.path.join(out_directory, filename)
        plt.savefig(outpath)
    else:
        plt.show()


def plot_topic_cumulative_recall(topic, runfile, out_directory):
    """Read in a topic ranking from a run and plot cumulative recall"""

    p = plt.subplot()
    p.plot(, label='cumulative recall', color='black')
    # p.plot(df_best / df_best.ix[0], label='Best', color='blue')
    p.set_title("Benchmark and Best Possible Strategies")
    p.grid(True)
    p.set_ylabel("Normalized Portfolio Value")
    p.set_xlabel("Date")
    p.legend(loc="upper left")

    filename = "chart-cr-{}-{}.png".format(topic, runfile)
    chart(filename, out_directory)


if __name__ == "__main__":

    topic = ""
    runfile = "../output/run-file-WAX-dev-Test-A.txt"
    out_directory = "../output/"
    out_directory = None
    plot_topic_cumulative_recall(topic, runfile, out_directory)


