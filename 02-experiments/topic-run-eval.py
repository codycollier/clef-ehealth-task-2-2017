#!/usr/bin/env python
"""Calculate evaluation metrics for a topic run


"""

import cet2_inputs
import cet2_output
import evals



if __name__ == "__main__":

    #  Params
    run_id = "Test-A"
    tag = "WAX-dev"
    path_docs = "../downloads/pubmed-docs-dev/"
    path_qrels = "../downloads/Training Data/qrel_abs_train"
    run_out_path = "../output/"

    # Load the docids / qrels for all topics
    topic_qrels = cet2_inputs.load_all_qrels(path_qrels)
    runs = load_run_file(outpath=run_out_path, run_id=run_id, tag=tag)

    # Run simulation for each topic
    for topic, qrelsets in topic_qrels.iteritems():

        qrel_pos_docids = qrelsets['pos']
        qrel_neg_docids = qrelsets['neg']
        topic_docids = qrelsets['all']

        # load the results?
        topic_run = runs[topic]
        evals.cumulative_return(topic_run, topic_qrels, debug=True)

        break
