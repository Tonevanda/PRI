#!/bin/bash

# This script expects a container started with the following command.
docker run --rm -p 8983:8983 --name onepiece_solr -v "${PWD}:/data" -d solr:9 solr-precreate episodes

# Creates a new core
docker exec onepiece_solr bin/solr create_core -c def_episodes

# Guarantess that no default fields are added
#curl http://localhost:8983/solr/def_episodes/config -d '{"set-user-property": {"update.autoCreateFields":"false"}}'

# Add a delay to ensure Solr is fully up and running
sleep 5

# Update synonyms.txt
docker cp ./data/synonyms.txt onepiece_solr:/var/solr/data/episodes/conf/synonyms.txt

# Schema definition via API
curl -X POST -H 'Content-type:application/json' \
    --data-binary "@./data/schema.json" \
    http://localhost:8983/solr/episodes/schema

# Default Schema definition via API
curl -X POST -H 'Content-type:application/json' \
    --data-binary "@./data/default_schema.json" \
    http://localhost:8983/solr/def_episodes/schema

# Add params
curl -X POST -H 'Content-type:application/json' \
    --data-binary "@./data/params.json" \
    http://localhost:8983/solr/episodes/config/params

# Add params to Default core
curl -X POST -H 'Content-type:application/json' \
    --data-binary "@./data/params.json" \
    http://localhost:8983/solr/def_episodes/config/params

# Update default parameters with the ones added
curl -X POST -H "Content-Type: application/json" \
    http://localhost:8983/solr/episodes/config/requestHandler \
    --data-binary '{
    "update-requesthandler": {
        "name": "/select",
        "class": "solr.SearchHandler",
        "defaults": {
            "paramset": "params"
        }
    }
    }'

# Update default parameters of the default core with the ones added
curl -X POST -H "Content-Type: application/json" \
    http://localhost:8983/solr/def_episodes/config/requestHandler \
    --data-binary '{
    "update-requesthandler": {
        "name": "/select",
        "class": "solr.SearchHandler",
        "defaults": {
            "paramset": "default_params"
        }
    }
    }'

# Index data
curl -X POST -H 'Content-type:application/json' \
    --data-binary "@./data/data_embeddings.json" \
    http://localhost:8983/solr/episodes/update?commit=true

# Index data in default core
curl -X POST -H 'Content-type:application/json' \
    --data-binary "@./data/data_embeddings.json" \
    http://localhost:8983/solr/def_episodes/update?commit=true
