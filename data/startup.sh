#!/bin/bash

# This script expects a container started with the following command.
docker run -p 8983:8983 --name meic_solr -v %cd%:/data -d solr:9 solr-precreate courses

# Schema definition via API
curl -X POST -H 'Content-type:application/json' \
    --data-binary "@./simple_schema.json" \
    http://localhost:8983/solr/courses/schema

# Populate collection using mapped path inside container.
docker exec -it meic_solr bin/post -c courses /data/data.csv

# Apontamentos
# Versões corretas para windows
# Create a core
docker exec meic_solr bin/solr create -c courses   
curl http://localhost:8983/solr/courses/schema -H "Content-type:application/json" -T "schema.json" -X POST
curl http://localhost:8983/solr/courses/update?commit=true -H "Content-type:application/json" -T "meic_courses.json" -X POST
curl http://localhost:8983/solr/courses/schema/fields/title -X GET 



