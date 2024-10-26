# PRI - One Piece Search Engine

## Requirements
Run ``pip install -r requirements.txt`` to install the dependencies

## Preparations

Start environment
```
prienv/Scripts/activate
```
Run requirements.txt

## M1. Data Preparation

We will use the data from episodes stored at the [wiki](https://onepiece.fandom.com/wiki/Episode_1). From this we will collect:

- Title
- Episode Number
- Season Number
- Arc
- Saga
- Air Date
- Opening
- Ending
- Long Summary

From this, we will have, at least:
- 1120 episodes (therefore the same amount of unique values such as title or long summary)
- 21 seasons
- 53 arcs
- 11 sagas
- 26 openings
- 20 endings

## Solr

### How To Run
#### Windows

There are many ways, try different ones until they work
1. run ``startup.bat``, open http://localhost:8983/solr/#/
2. Inside ``git bash``, run ``sh startup.sh``, open http://localhost:8983/solr/#/

### Versões corretas dos comandos para windows
#### Create a core
docker exec meic_solr bin/solr create -c courses   
#### Load schema
curl http://localhost:8983/solr/courses/schema -H "Content-type:application/json" -T "schema.json" -X POST
#### Load data
curl http://localhost:8983/solr/courses/update?commit=true -H "Content-type:application/json" -T "meic_courses.json" -X POST
#### Get Operation
curl http://localhost:8983/solr/courses/schema/fields/title -X GET 