#!/bin/bash

# This script expects a container started with the following command.
docker run --rm -p 8983:8983 --name onepiece_solr -v "${PWD}:/data" -d solr:9 solr-precreate episodes

# Add a delay to ensure Solr is fully up and running
sleep 5

# Update synonyms.txt
docker cp ./data/synonyms.txt onepiece_solr:/var/solr/data/episodes/conf/synonyms.txt

# Schema definition via API
curl -X POST -H 'Content-type:application/json' \
    --data-binary "@./data/schema.json" \
    http://localhost:8983/solr/episodes/schema

# Check if running on Windows and use winpty if necessary
#if [[ "$OSTYPE" == "msys" ]]; then
#    winpty docker exec -it onepiece_solr bin/solr post -c episodes /data/data.csv
#else
#    docker exec -it onepiece_solr bin/solr post -c episodes /data/data.csv
#fi

curl -X POST -H 'Content-type:text/csv' \
    --data-binary "@./data/data.csv" \
    http://localhost:8983/solr/episodes/update?commit=true
