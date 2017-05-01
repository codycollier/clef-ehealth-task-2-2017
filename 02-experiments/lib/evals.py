"""Evaluation helpers

ref:
    topic inter pubmedid rank score run-id
    CD009944 AF 22407696 764 0.130718954248 Test-A
    CD009944 AF 22370214 765 0.130548302872 Test-A
    CD009944 AF 22302678 766 0.13037809648 Test-A
    CD009944 AF 22214545 767 0.130208333333 Test-A
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


def plot_topic_cumulative_recall(cr, topic, run_id, phase, tag, out_directory=None):
    """Plot cumulative recall for a topic"""

    p = plt.subplot()
    ranks, cr_vals = zip(*cr)
    p.plot(ranks, cr_vals, label='cumulative recall', color='green')
    p.set_title("Cumulative Recall - {} - {} - {} ({})".format(topic, run_id, phase, tag))
    p.grid(True)
    p.set_ylabel("Cumulative recall")
    p.set_xlabel("Rank of Items Reviewed")
    p.legend(loc="upper left")

    filename = "chart-cr-{}-{}-{}.png".format(tag, topic, run_id)
    chart(filename, out_directory)


def cumulative_return(topic_run, topic_qrels, debug=False):
    """Calculate cumulative return for a topic run ranking"""
    # cr = [(rank, cr), ...]
    cr_list = []
    cr = 0
    print(topic_qrels['pos'])
    for docid, rank, score in topic_run:
        if docid in topic_qrels['pos']:
            cr += 1
        cr_list.append((rank, cr))
        if debug:
            print((rank, cr))
    return cr_list


if __name__ == "__main__":

    # ad hoc testing if called directly
    pass


