#!/bin/bash

# This script expects a container started with the following command.
docker run --rm -p 8983:8983 --name onepiece_solr -v "${PWD}:/data" -d solr:9 solr-precreate episodes

# Add a delay to ensure Solr is fully up and running
sleep 5

# Schema definition via API
curl -X POST -H 'Content-type:application/json' \
    --data-binary "@./data/default_schema.json" \
    http://localhost:8983/solr/episodes/schema

curl -X POST -H 'Content-type:text/csv' \
    --data-binary "@./data/data.csv" \
    http://localhost:8983/solr/episodes/update?commit=true
