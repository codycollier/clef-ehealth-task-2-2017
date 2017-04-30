#!/usr/bin/env python
"""Download the pubmed docids in batches and then split them into single files

Assumes:
     This has been run:
        ./01-get-unique-pubmed-ids.sh

     And these output files exist (one id per line):
        ./list-of-pubmed-ids-dev
        ./list-of-pubmed-ids-test

"""

import os.path
import sys
import time

import requests


def make_batches(docid_filename, N=10):
    """Generate batches of N docids"""
    with open(docid_filename) as df:
        dcount = 0
        docids = []
        for docid in df:
            docids.append(docid.strip())
            dcount += 1
            if dcount >= N:
                yield docids
                docids = []
                dcount = 0
        yield docids


def get_batch(docids):
    """Download batch of pubmed docids in MEDLINE and txt form

    ref:
    curl -XPOST -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=${docs_csv}&rettype=medline&retmode=text
    """

    docs_csv = ",".join([str(d) for d in docids])
    uri = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={0}&rettype=medline&retmode=text".format(docs_csv)
    results = requests.post(uri)

    # safety
    if results.status_code != requests.codes.ok:
        print("Bad Response from pubmed server...")
        print(results.status_code)
        print(results.headers)
        print(results.text)
        sys.exit(100)

    return results.text


def write_batch(raw_results, directory):
    """Split the results by empty lines and write to separate files by pubmed id"""

    def write_file(lines, directory):
        line1 = filelines[0]   # ex: "PMID- 9990351"
        pmid = line1.split(" ")[-1]
        filename = os.path.join(directory, "{0}.medline.txt".format(pmid))
        contents = "\n".join(filelines)
        with open(filename, 'w') as of:
            of.write(contents)

    filelines = []
    for raw_line in raw_results.split("\n"):
        line = raw_line.strip()
        if line != "":
            # If not empty line, just keep consuming raw lines
            filelines.append(line)
        else:
            # if empty line after good lines, stop and write contents to file
            if len(filelines) > 0:
                filelines.append("")
                write_file(filelines, directory)
                filelines = []

    # catch the last file
    if len(filelines) > 0:
        filelines.append("")
        write_file(filelines, directory)
        filelines = []

    return


if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("")
        print("Usage:")
        print("  {} <list-of-pubmed-ids> <output-dir>".format(sys.argv[0]))
        print("Example:")
        print("  {} ./list-of-pubmed-ids-dev ../downloads/pubmed-docs-dev/".format(sys.argv[0]))
        print("")
        sys.exit(1)

    docid_filename = sys.argv[1]    # docid_filename = "./list-of-pubmed-ids-dev"
    directory = sys.argv[2]         # directory = "../downloads/pubmed-docs-dev/"

    if not os.path.exists(directory):
        print("Error: output directory does not exist")
        sys.exit(1)

    for batch_count, docids in enumerate(make_batches(docid_filename, N=500)):
        print("batch {0}".format(batch_count))
        raw_results = get_batch(docids)
        write_batch(raw_results, directory)
        time.sleep(5)



