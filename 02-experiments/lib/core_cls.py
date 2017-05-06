"""Run a simulation using classification model(s) and...


ref:
    http://scikit-learn.org/stable/modules/feature_extraction.html
    http://scikit-learn.org/stable/modules/tree.html
    http://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html
    http://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeRegressor.html
"""

import random
import time
import sys

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.tree import DecisionTreeClassifier

import cet2_inputs
import cet2_output


def file_paths(docids, dpath):
    tdocs = []
    for docid in docids:
        tfile = "{}/{}.medline.txt".format(dpath, docid)
        tdocs.append(tfile)
    return tdocs


def file_handles(docs):
    for doc in docs:
        yield open(doc, 'r')


def build_model_and_rank(pos, neg, unk, docpath, model="dectree", debug=False):
    """Build a classifier from the pos/neg docs and rank the unknown docs

    """

    pos_docids = list(pos)
    neg_docids = list(neg)
    unk_docids = list(unk)

    all_docids = pos_docids[:]
    all_docids.extend(neg_docids)
    all_docids.extend(unk_docids)
    all_docs = file_paths(all_docids, docpath)

    # --------------------------------------------------------------
    #  Create features from the docs
    # --------------------------------------------------------------

    # Fit the vectorizer on all the docs
    vectorizer = CountVectorizer(input="file")
    vectorizer.fit(file_handles(all_docs))

    # Create X (features) from the labeled docs
    lab_docids = pos_docids[:]
    lab_docids.extend(neg_docids)
    X_lab = vectorizer.transform(file_handles(file_paths(lab_docids, docpath)))

    # Create Y (labels) for the labeled docs
    Y_lab = [1 for i in pos_docids]
    Y_lab.extend([-1 for i in neg_docids])

    # Vectorize the unknown docids for prediction later
    X_unk = vectorizer.transform(file_handles(file_paths(unk_docids, docpath)))

    if debug and False:
        print type(X_lab)
        for i, feature_vec in enumerate(X_lab):
            print("fv:", feature_vec)
            if i >= 5:
                break

    # --------------------------------------------------------------
    #  Build the model from the labeled docs
    # --------------------------------------------------------------
    if model == "dectree":
        m = DecisionTreeClassifier()
        m.fit(X_lab, Y_lab)
    else:
        raise Exception("Invalid model selection")

    # --------------------------------------------------------------
    #  DEBUG - pos should be predictid pos
    # --------------------------------------------------------------
    if debug:
        X_pos = vectorizer.transform(file_handles(file_paths(pos_docids, docpath)))
        X_neg = vectorizer.transform(file_handles(file_paths(neg_docids, docpath)))

        print("predicting...")

        p = m.predict(X_pos)
        print("positive: ", p)

        p = m.predict(X_neg)
        print("negative: ", p)

    # --------------------------------------------------------------
    #  Classify/Rank the remaining docs
    # --------------------------------------------------------------
    P = m.predict(X_unk)
    if debug:
        print("unknowns: ", P)
    return (unk_docids, P)


def run_sim(topic, qrel_pos_docids, qrel_neg_docids, topic_docids, path_docs, model="dectree", debug=False):
    """Run a simulation of a review for a given topic

    """

    review_log = []
    reviewed_all = set()
    reviewed_pos = set()
    reviewed_neg = set()
    review_round = 0
    empty_pos_rounds = 0
    classification = []
    keep_reviewing = True

    # key parameters
    debug = True
    min_pos = 1
    batch_count = 10
    empty_pos_rounds_max = 10

    start = time.time()
    while keep_reviewing:

        review_round += 1
        if debug:
            print("::{}".format("-" * 80))
            print("::  {} - Review Round: {}".format(topic, review_round))
            print("::{}".format("-" * 80))

        reviewed_this_round = []

        # In round 1, sample randomly until there's at least 1 positive doc
        if review_round == 1:
            found_pos = 0
            while found_pos < min_pos:
                reviewed_this_round.extend(random.sample(topic_docids, batch_count))
                for d in reviewed_this_round:
                    if d in qrel_pos_docids:
                        found_pos += 1
                        if found_pos >= min_pos:
                            break

        # In other rounds, take all the pos predictions or at least topN
        else:
            # ...top N from the list
            topN = zip(*classification[:batch_count])[1]
            if debug:
                print("topN:", topN)

            # ...the pos predictions
            posN = [docid for pred, docid in classification if pred == 1]
            if len(posN) == 0:
                empty_pos_rounds += 1
            else:
                empty_pos_rounds = 0
            if debug:
                print("posN:", posN)

            # run-A
            # if len(posN) > len(topN):
            #     reviewed_this_round.extend(posN)
            # else:
            #     reviewed_this_round.extend(topN)

            # run-B
            if len(posN) > len(topN):
                reviewed_this_round.extend(posN)
            elif len(posN) > 0:
                reviewed_this_round.extend(topN)
            else:
                rdoc = zip(*classification)[1]
                reviewed_this_round.extend(random.sample(rdoc, batch_count))

        # Collect the reviewed docs
        for d in reviewed_this_round:
            review_log.append(d)
            reviewed_all.add(d)
            if d in qrel_pos_docids:
                reviewed_pos.add(d)
            else:
                reviewed_neg.add(d)
        reviewed_not = topic_docids - reviewed_all

        if debug:
            print("topic_docids: {}".format(len(topic_docids)))
            print("reviewed_not: {}".format(len(reviewed_not)))
            print("reviewed_all: {}".format(len(reviewed_all)))
            print("reviewed_pos: {}".format(len(reviewed_pos)))
            print("reviewed_neg: {}".format(len(reviewed_neg)))

        X_unk, P = build_model_and_rank(reviewed_pos, reviewed_neg, reviewed_not, path_docs, model, debug=False)
        classification = zip(P, X_unk)
        classification.sort(reverse=True)

        # How to determine stop and/or convergence-like state?
        if len(reviewed_not) < batch_count:
            keep_reviewing = False
            if debug:
                print("done reviewing: less than a full batch of docs left")

        elif empty_pos_rounds >= empty_pos_rounds_max:
            keep_reviewing = False
            if debug:
                print(":::{}".format("-" * 80))
                print("::: topic: {}  rounds: {}  reviewed: {} of {}".format(topic, review_round, len(reviewed_all), len(topic_docids)))
                print("::: done reviewing: max rounds of empty positive docs in classification")
                print("::: elapsed: {} s".format(time.time() - start))
                print(":::{}".format("-" * 80))

        # end of round
        if debug:
            sys.stdout.flush()

    # end of topic reviewing
    return review_log, reviewed_not, reviewed_all, reviewed_pos, reviewed_neg


if __name__ == "__main__":

    pass

