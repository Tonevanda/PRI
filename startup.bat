docker run --rm -p 8983:8983 --name onepiece_solr -v %cd%:/data -d solr:9 solr-precreate episodes

timeout /t 1

curl http://localhost:8983/solr/episodes/schema -H "Content-type:application/json" -T "schema.json" -X POST
::curl http://localhost:8983/solr/episodes/schema \
::    -H "Content-type:application/json" \
::    -T "schema.json" -X POST

curl http://localhost:8983/solr/episodes/update?commit=true -H "Content-type:text/csv" -T "./data/data.csv" -X POST
::curl http://localhost:8983/solr/episodes/update?commit=true \
::    -H "Content-type:text/csv" \
::    -T "./data/data.csv" -X POST

timeout /t 1000