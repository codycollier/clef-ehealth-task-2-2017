#!/usr/bin/env bash
#
# . get the unique set of pubmed ids from the dev/test set
#

cd $(dirname $0)
mkdir -p ../downloads/pubmed-docs-dev/

if [ ! -f ./list-of-pubmed-ids-dev ]; then
    cat ../downloads/Training\ Data/qrel_* | tr -s ' ' | cut -f3 -d" " | sort | uniq > list-of-pubmed-ids-dev
fi
ls -la list-of-pubmed-ids-dev


