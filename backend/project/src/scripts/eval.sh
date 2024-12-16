rm -rf results
rm -rf diagrams
rm -rf qrels
mkdir diagrams
mkdir results
mkdir qrels
python pipeline.py --query ./query.json --topk 520 --score avg --reRankDocs 30 --reRankWeight 95 --gridSearch False