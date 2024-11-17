rm -rf results
rm -rf diagrams
rm -rf qrels
mkdir diagrams
mkdir results
mkdir qrels
python ../src/scripts/pipeline.py --query ./query.json