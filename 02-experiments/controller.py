#!/usr/bin/env python
"""Main controller to run a simulation or look at results


"""

import sys

import cet2_inputs
import cet2_output
import core_cls
import evals


def usage(error=None):
    """Show usage and exit"""
    print("")
    if error:
        print("Error: {}".format(error))
        print("")
    print("Usage: {} <action> <setname> <run-id> <tag>".format(sys.argv[0]))
    print("Example: {} sim dev turtle 'try-stop-10'".format(sys.argv[0]))
    print("Example: {} sim dev mole 'try-stop-03'".format(sys.argv[0]))
    print("Example: {} sim dev cat 'submit'".format(sys.argv[0]))
    print("Example: {} sim test cat 'submit'".format(sys.argv[0]))
    print("")
    sys.exit(1)


if __name__ == "__main__":

    # Incoming params
    if not len(sys.argv) == 3:
        usage()
    else:
        action = sys.argv[1]
        setname = sys.argv[2]
        run_id = sys.argv[3]
        tag = sys.argv[4]

    # validate
    valid_actions = ("sim", "eval")
    if action not in valid_actions:
        usage(error="Must use action in {}".format(valid_actions))
    valid_setnames = ("dev", "test")
    valid_runids = ("turtle", "crane")
    if setname not in valid_setnames:
        usage(error="Must use setname in {}".format(valid_setnames))
    if run_id not in valid_runids:
        usage(error="Must use run-id in {}".format(valid_runids))

    if run_id == "turtle":
        protocol = 1
        model = "dectree"
        # run_id = "run-A"    # run-A - all pos or top N - stop 03 empty
        # run_id = "run-A"    # run-A - all pos or top N - stop 10 empty
        run_id = "run-B"    # run-A - all pos or top N w/ pos or random - stop 10 empty

    elif run_id == "crane":
        protocol = 1
        model = "dectree"

    if setname == "dev":
        path_docs = "../downloads/pubmed-docs-dev/"
        path_qrels = "../downloads/Training Data/qrel_abs_train"
    elif setname == "test":
        path_docs = "../downloads/pubmed-docs-test/"
        path_qrels = "../downloads/---TBD---/"

    team = "WAX"
    run_out_path = "../output/"

    team_run_id = "{}-{}".format(team, run_id)
    run_slug = "{}-{}-tag-{}".format(setname, team_run_id, tag)

    # Load the docids / qrels for all topics
    topic_qrels = cet2_inputs.load_all_qrels(path_qrels)
    if action == "eval":
        runs = cet2_output.load_run_file(outpath=run_out_path, run_slug=run_slug)

    if action == "sim":

        # Run simulation for each topic
        for topic, topic_qrelsets in topic_qrels.iteritems():

            qrel_pos_docids = topic_qrelsets['pos']
            qrel_neg_docids = topic_qrelsets['neg']
            topic_docids = topic_qrelsets['all']

            # TODO - add timing
            results = core_cls.run_sim(topic, qrel_pos_docids, qrel_neg_docids, topic_docids, path_docs=path_docs, model=model, debug=True)
            review_log, reviewed_not, reviewed_all, reviewed_pos, reviewed_neg = results
            print("")

            topic_lines = cet2_output.gen_trec_topic_run(topic, review_log, run_id=run_id, debug=True)
            cet2_output.write_run_file(topic_lines, outpath=run_out_path, run_slug=run_slug)
            print("")

    elif action == "eval":

        # Run a simple eval and chart the topic results for quick inspection
        #  See the official eval script from lab hosts for more detail (tar_eval.py)
        for topic, topic_qrelsets in topic_qrels.iteritems():

            print(topic)
            print(type(runs))
            topic_run = runs[topic]
            cr = evals.cumulative_return(topic_run, topic_qrelsets, debug=False)
            evals.plot_topic_cumulative_recall(cr, topic, run_id, setname, team, out_directory=None)



