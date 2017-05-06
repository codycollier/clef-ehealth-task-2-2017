#!/usr/bin/env python
"""Main controller to run a simulation or look at results


"""

import os.path
import sys
import time

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
    if not len(sys.argv) == 5:
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
    total_topics = len(topic_qrels.keys())
    if action == "eval":
        runs = cet2_output.load_run_file(outpath=run_out_path, run_slug=run_slug)

    # Take the designated action
    if action == "sim":

        # Don't overwrite/append data to existing file
        outfile = os.path.join(run_out_path, "run-file-{}.txt".format(run_slug))
        if os.path.exists(outfile):
            raise Exception("The output run file already exists ({})".format(outfile))

        # Run simulation for each topic
        start_total = time.time()
        for i, (topic, topic_qrelsets) in enumerate(topic_qrels.iteritems()):

            # Header
            print(":{}".format("-" * 80))
            print(": Starting: {} - topic {} of {}".format(topic, i, total_topics))
            print(":{}".format("-" * 80))

            # Simulation
            qrel_pos_docids = topic_qrelsets['pos']
            qrel_neg_docids = topic_qrelsets['neg']
            topic_docids = topic_qrelsets['all']
            start_sim = time.time()

            if run_id == "turtle":
                results = core_cls.run_sim(topic, qrel_pos_docids, qrel_neg_docids, topic_docids, path_docs=path_docs, model=model, debug=True)
            elif run_id == "crane":
                pass
            review_log, reviewed_not, reviewed_all, reviewed_pos, reviewed_neg = results

            topic_lines = cet2_output.gen_trec_topic_run(topic, review_log, run_id=team_run_id, debug=False)
            cet2_output.write_run_file(topic_lines, outpath=run_out_path, run_slug=run_slug)

            # Footer
            elapsed_sim = time.time() - start_sim
            elapsed_total = time.time() - start_total
            print(":{}".format("-" * 80))
            print(": ")
            print(": sim time elapsed: {} seconds ({})".format(elapsed_sim, topic))
            print(": Finished: {} - topic {} of {}".format(topic, i, total_topics))
            print(": ")
            print(": total time elapsed: {} seconds".format(elapsed_total))
            print(": ")
            print(":{}".format("-" * 80))

            # debug
            break

    elif action == "eval":

        # Run a simple eval and chart the topic results for quick inspection
        #  See the official eval script from lab hosts for more detail (tar_eval.py)
        for topic, topic_qrelsets in topic_qrels.iteritems():

            print(topic)
            print(type(runs))
            topic_run = runs[topic]
            cr = evals.cumulative_return(topic_run, topic_qrelsets, debug=False)
            evals.plot_topic_cumulative_recall(cr, topic, run_id, setname, team, out_directory=None)

            # debug
            break


