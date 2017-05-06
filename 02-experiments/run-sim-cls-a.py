#!/usr/bin/env python
"""Main controller to run a simulation using classification model(s)


"""

import cet2_inputs
import cet2_output
import core_cls


if __name__ == "__main__":

    #  Params
    # run_id = "run-A"    # run-A - all pos or top N - stop 03 empty
    # run_id = "run-A"    # run-A - all pos or top N - stop 10 empty
    run_id = "run-B"    # run-A - all pos or top N w/ pos or random - stop 10 empty
    tag = "WAX-dev"
    model = "dectree"
    path_docs = "../downloads/pubmed-docs-dev/"
    path_qrels = "../downloads/Training Data/qrel_abs_train"
    run_out_path = "../output/"

    # Load the docids / qrels for all topics
    topic_qrels = cet2_inputs.load_all_qrels(path_qrels)

    # Run simulation for each topic
    for topic, qrelsets in topic_qrels.iteritems():

        qrel_pos_docids = qrelsets['pos']
        qrel_neg_docids = qrelsets['neg']
        topic_docids = qrelsets['all']

        results = core_cls.run_sim(topic, qrel_pos_docids, qrel_neg_docids, topic_docids, path_docs=path_docs, model=model, debug=True)
        review_log, reviewed_not, reviewed_all, reviewed_pos, reviewed_neg = results
        print("")

        topic_lines = cet2_output.gen_trec_topic_run(topic, review_log, run_id=run_id, debug=True)
        cet2_output.write_run_file(topic_lines, outpath=run_out_path, run_id=run_id, tag=tag)
        print("")

