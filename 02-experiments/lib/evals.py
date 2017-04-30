"""Evaluation helpers

ref:
    topic inter pubmedid rank score run-id
    CD009944 AF 22407696 764 0.130718954248 Test-A
    CD009944 AF 22370214 765 0.130548302872 Test-A
    CD009944 AF 22302678 766 0.13037809648 Test-A
    CD009944 AF 22214545 767 0.130208333333 Test-A
"""


def cumulative_return(topic_run, topic_qrels, debug=False):
    """Calculate cumulative return for a topic run ranking"""
    # cr = [(rank, cr), ...]
    cr_list = []
    cr = 0
    for docid, rank, score in topic_run:
        if docid in topic_qrels['pos']:
            cr += 1
        cr_list.append((rank, cr))
    return cr_list


if __name__ == "__main__":

    # ad hoc testing if called directly
    pass


