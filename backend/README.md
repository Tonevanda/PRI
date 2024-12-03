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

To stop, simply do ```docker stop onepiece_solr```. The docker will also remove it. To check if it was properly removed, do ```docker ps -a```

### Versões corretas dos comandos para windows
#### Create a core
docker exec meic_solr bin/solr create -c courses   
#### Load schema
curl http://localhost:8983/solr/courses/schema -H "Content-type:application/json" -T "schema.json" -X POST
#### Load data
curl http://localhost:8983/solr/courses/update?commit=true -H "Content-type:application/json" -T "meic_courses.json" -X POST
#### Get Operation
curl http://localhost:8983/solr/courses/schema/fields/title -X GET

## M2. Schema

Find all possible schema options [here](https://solr.apache.org/guide/solr/latest/indexing-guide/filters.html)

### Field Types

#### text

- "class":"solr.TextField": Good for when we need to perform full-text searches and we need to do text analysis features such as stemming and stop word removal.
- "positionIncrementGap":"100": Needed when using multiValued fields (Full_Text), to ensure it doesn't produce false positives. i.e. Value 1: "Monkey D. Luffy sets out to become the Pirate King." / Value 2: "He recruits Zoro and navigates the Grand Line.". Without the gap, a query such as "Pirate King He recruits" might match because there's no positional gap, even though "He" comes from the second value.
- analyzer: Does the following in both the query and indexing
    - "class":"solr.StandardTokenizerFactory": splits text into tokens based on standard grammar.
    - "class":"solr.ASCIIFoldingFilterFactory": Converts non-ASCII characters to their ASCII equivalents.
    - "class": "solr.LowerCaseFilterFactory": Converts all tokens to lowercase for case-insensitive searching.
    - "class": "solr.StopFilterFactory": Removes common English stop words
    - "class": "solr.PorterStemFilterFactory": Reduces words to their root form (i.e., "pirates" to "pirate")
    - "class": "solr.PhoneticFilterFactory": To handle misspellings and provide more flexible search results. This filter helps match similar-sounding words, enhancing the user experience by providing more relevant search results.

#### small_text
- "class":"solr.StrField": Good for fields where the exact value is important, and no text analysis is needed.
- sortMissingLast: Ensures that documents with missing values for this field are sorted last when sorting in ascending order.
- docValues: Enables efficient sorting and faceting.

#### number
- "class":"solr.FloatPointField": Used for numeric fields where floating-point precision is required.
- docValues: Enables efficient sorting and faceting.

#### date
- "class":"solr.DatePointField": Used for date fields.
- docValues: Enables efficient sorting and faceting.

### Field Definitions
We define what kind of field type each field will use, in order to use the correct analyzers. We also add a Full_Text multivalued field that uses all text elements for an improved search method across all fields.

- indexed: True and it will be searchable
- stored: True and it can be retrieved in results
- multivalued: True and will be able to have multiple values

### Copy Field
Copies contents from one field to another. We use this to add all the text elements to a single one to improve querying.

## M2. Schema -> Ideas to improve schema:
- KeywordMarkerFilterFactory: Protects words from being modified by stemmers.
- Synonymns...
