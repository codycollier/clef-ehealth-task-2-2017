#!/usr/bin/env python
"""Calculate evaluation metrics for a topic run


"""

import cet2_inputs
import cet2_output
import evals


if __name__ == "__main__":

    #  Params
    run_id = "run-A"
    tag = "WAX-dev"
    ttag = "WAX"
    phase = "dev"
    path_docs = "../downloads/pubmed-docs-dev/"
    path_qrels = "../downloads/Training Data/qrel_abs_train"
    run_out_path = "../output/"

    # Load the docids / qrels for all topics
    topic_qrels = cet2_inputs.load_all_qrels(path_qrels)
    runs = cet2_output.load_run_file(outpath=run_out_path, run_id=run_id, tag=tag)

    # Run simulation for each topic
    for topic, topic_qrelsets in topic_qrels.iteritems():

        print(topic)
        print(type(runs))
        topic_run = runs[topic]
        cr = evals.cumulative_return(topic_run, topic_qrelsets, debug=False)
        evals.plot_topic_cumulative_recall(cr, topic, run_id, phase, ttag, out_directory=None)

        break
