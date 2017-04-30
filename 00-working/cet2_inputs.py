#!/usr/bin/env python
"""Helpers for the custom CLEF eHealth Task 2 file formats

"""

import os
import os.path
from collections import defaultdict


def load_topic_numbers(topic_path):
    """Read the list of topic files and then load all the topic numbers

    This is tailored to the CLEF eHealth Task 2 formats

    example:
    $head -30 ../Training\ Data/topics_train/1
    Topic: CD010438

    Title: Thromboelastography (TEG) and rotational thromboelastometry (ROTEM)
    for trauma-induced coagulopathy in adult trauma patients with bleeding

    Query:
    (Thrombelastogra$ or Thromboelastogra$ or (thromb$ adj2 elastogra$) or TEG or haemoscope or haemonetics).mp
    Thrombelastography/
    (thromboelasto$ or thrombelasto$ or (thromb$ adj2 elastom$) or (rotational adj2 thrombelast) or ROTEM or "tem international").mp.
    1 or 2 or 3
    exp animals/ not humans.sh.
    4 not 5
    limit 6 to yr="1970 -Current"

    Pids:
        23446185
        23425732
        23410777
        23407150
        23385320
        23354242
        23354228
        23354227
        23351534
        23321555
        23316863
        23313481
        23302970
        23302040
        23301972
        23301969
    """
    if not os.path.exists(topic_path):
        raise ValueError("Not a valid topic directory")

    topics_to_numbers = {}
    for topic_number in os.listdir(topic_path):
        topic_file = os.path.join(topic_path, topic_number)
        if not os.path.isfile(topic_file):
            continue

        topic = None
        with open(topic_file, 'r') as tf:
            for line in tf:
                if 'Topic:' in line:
                    topic = line.strip().split(" ")[1]
                    break
        topics_to_numbers[topic] = int(topic_number)

    return topics_to_numbers


def load_all_qrels(qrel_path):
    """Read a qrels file and load the topics->docids->judgements

    This is tailored to the CLEF eHealth Task 2 formats

    example:
    $head ../Training\ Data/qrel_abs_train
    CD010438     0  4461416      0
    CD010438     0  19762299     0
    CD010438     0  16607076     0
    CD010438     0  20042049     0
    CD010438     0  7223223      0
    CD010438     0  21330915     0
    CD010438     0  4576350      0
    CD010438     0  20813396     0
    CD010438     0  12675727     0
    CD010438     0  22782135     0
    """
    if not os.path.exists(qrel_path):
        raise ValueError("Not a valid qrel file path")

    topic_qrels = defaultdict(lambda: defaultdict(set))
    with open(qrel_path, 'r') as qrfile:
        for line in qrfile:
            # parts = line.strip().split()
            topic, unk, pubmedid, pos = line.strip().split()
            pos = int(pos)
            topic_qrels[topic]['all'].add(pubmedid)
            if pos:
                topic_qrels[topic]['pos'].add(pubmedid)
            else:
                topic_qrels[topic]['neg'].add(pubmedid)
    return topic_qrels


if __name__ == "__main__":

    # Ad hoc testing if called directly

    # 4.7M    ../Training Data/qrel_abs_train
    # 4.7M    ../Training Data/qrel_content_train
    # 1.9M    ../Training Data/topics_train

    path = "../downloads/Training Data/topics_train/"
    topics_to_numbers = load_topic_numbers(path)
    print("")
    print("topics to numbers:")
    print(topics_to_numbers)
    print("topic count: {}".format(len(topics_to_numbers)))
    print("")

    # path = "../downloads/Training Data/qrel_content_train"
    path = "../downloads/Training Data/qrel_abs_train"
    topic_qrels = load_all_qrels(path)
    print("")
    print("topics to pubmed qrels:")
    count = 0
    for topic, qrels in topic_qrels.iteritems():
        count += 1
        print("")
        for qtype in ('all', 'neg', 'pos'):
            qr_docids = qrels[qtype]
            print("{} - {} - {} ({}...)".format(topic, qtype, len(qr_docids), list(qr_docids)[:5]))
    print("")
    print("topic count: {}".format(count))
    print("")




