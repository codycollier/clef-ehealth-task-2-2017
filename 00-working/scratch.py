#!/usr/bin/env python
"""

ref:
    http://scikit-learn.org/stable/modules/feature_extraction.html
"""


import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeClassifier


def file_paths(docids):
    tpath = "./pubmed-docs-dev/"
    tdocs = []
    for docid in docids:
        tfile = "{}/{}.medline.txt".format(tpath, docid)
        tdocs.append(tfile)
    return tdocs


def file_handles(docs):
    for doc in docs:
        yield open(doc, 'r')


if __name__ == "__main__":

    # --------------------------------------------------------------
    #  Create features from the docs
    # --------------------------------------------------------------
    pos_docids = ["1834925", "12761010", "18347741"]
    neg_docids = ["14340441", "17649646"]
    unk_docids = ["14340868", "17649654", "20129067", "22948985", "6435019"]
    unk_docids = ["9799142", "9799149", "9799267", "9799344", "97997", "9799767",
            "97998", "97999", "9799994", "9799997", "9800067", "9800131", "9800243",
            "9800738", "9800934", "9800957", "9800974", "9800978", "9801085", "9801116",
            "9801126", "9801201", "9801220", "9801251", "9801252", "9801253", "9801256",
            "980128", "9801342", "9801343", "980144", "9801729", "9801736", "98018",
            "9801867", "9801929", "9801973", "9802042", "980212", "9802162", "9802169",
            "9802214", "9802344"]

    all_docids = pos_docids[:]
    all_docids.extend(neg_docids)
    all_docids.extend(unk_docids)
    all_docs = file_paths(all_docids)

    vectorizer = CountVectorizer(input="file")
    vectorizer.fit(file_handles(all_docs))
    print(vectorizer)

    lab_docids = pos_docids[:]
    lab_docids.extend(neg_docids)
    X_lab = vectorizer.transform(file_handles(file_paths(lab_docids)))
    y_lab = [1 for i in pos_docids]
    y_lab.extend([-1 for i in neg_docids])

    X_unk = vectorizer.transform(file_handles(file_paths(unk_docids)))

    # features = dict(zip(all_docids, X))
    # X_l = np.array([features[x] for x in l_docids])
    # X_u = np.array([features[x] for x in u_docids])

    print type(X_lab)
    for i, feature_vec in enumerate(X_lab):
        print("fv:", feature_vec)
        if i >= 5:
            break

    # --------------------------------------------------------------
    #  Build the model from the labeled docs
    # --------------------------------------------------------------
    m = DecisionTreeClassifier()
    m.fit(X_lab, y_lab)
    # m.fit(X_neg, y_neg)

    # --------------------------------------------------------------
    #  Classify/Rank the remaining docs
    # --------------------------------------------------------------

    X_pos = vectorizer.transform(file_handles(file_paths(pos_docids)))
    X_neg = vectorizer.transform(file_handles(file_paths(neg_docids)))

    print("predicting...")

    p = m.predict(X_pos)
    print("positive: ", p)

    p = m.predict(X_neg)
    print("negative: ", p)

    p = m.predict(X_unk)
    print("unknowns: ", p)






