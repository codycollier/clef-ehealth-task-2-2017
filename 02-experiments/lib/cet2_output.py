#!/usr/bin/env python
"""Helpers for the CLEF eHealth Task 2 output formats

ref:
    https://sites.google.com/site/clefehealth2017/task-2
"""

import os
import os.path


def gen_trec_topic_run(topic, reviewed_docs, run_id, debug=False):
    """Generate the ranked list and metadata for a single topic

    Run Format : TOPIC-ID    INTERACTION    PID    RANK    SCORE    RUN-ID

    TOPIC-ID can be found in the released topics.
    PID = PubMed Document Identifier.
    RANK = the rank of the document (in increasing order)
    SCORE = the score of the ranking/classification algorithm
    RUN-ID = an identifier for the submissio

    INTERACTION: The interaction field is still TBD. Some possibilities are below, but under consideration.
    simple evaluation version:
    INTERACTION = AF, relevance feedback is used by the system to compute the ranking of subsequent documents
    INTERACTION = NF, relevance feedback is not being used by the system
    INTERACTION = NS, the document is not shown to the user (these documents can be excluded from the output)

    """
    lines = []
    for rank, pubmedid in enumerate(reviewed_docs):
        score = 100 * (1.0 / (rank + 1))
        line = "{} {} {} {} {} {}".format(topic, "AF", pubmedid, rank, score, run_id)
        lines.append(line)
        if debug:
            print(line)
    return lines


def write_run_file(topic_lines, outpath="../output/", run_id="", tag="WAX-dev"):
    """Write out the run file"""

    if not os.path.exists(outpath):
        raise Exception("The output path for the run file doesn't exist")

    outfile = os.path.join(outpath, "run-file-{}-{}.txt".format(tag, run_id))
    with open(outfile, 'a') as out:
        out.write("\n".join(topic_lines))


if __name__ == "__main__":

    # Ad hoc testing if called directly
    pass



