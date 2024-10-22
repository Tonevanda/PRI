#!/bin/bash

# This script expects a container started with the following command.
docker run --rm -p 8983:8983 --name onepiece_solr -v ${PWD}:/data -d solr:9 solr-precreate episodes

# Schema definition via API
curl -X POST -H 'Content-type:application/json' \
    --data-binary "@./schema.json" \
    http://localhost:8983/solr/episodes/schema

#curl http://localhost:8983/solr/episodes/schema \
#    -H "Content-type:application/json" \
#    -T "schema.json" -X POST

# Populate collection using mapped path inside container.
docker exec -it onepiece_solr bin/post -c episodes /data/data.csv





