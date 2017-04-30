#!/usr/bin/env bash
#
# . get the unique set of pubmed ids from the dev/test set
#
# sed help:
# http://stackoverflow.com/questions/7103531/how-to-get-the-part-of-file-after-the-line-that-matches-grep-expression-first
#
#

cd $(dirname $0)
mkdir -p ../downloads/pubmed-docs-test/

if [ ! -f ./list-of-pubmed-ids-test ]; then
    sed -e '1,/Pids:/d' ../downloads/topics_test/* | tr -s ' ' | cut -f2 -d" " | sort | uniq > list-of-pubmed-ids-test
fi
ls -la list-of-pubmed-ids-test


