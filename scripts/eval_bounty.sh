python ../src/scripts/query_solr.py --query queries/bounty.json --uri http://localhost:8983/solr --collection episodes | \
python ../src/scripts/solr2trec.py > results_bounty_trec.txt

cat ../qrels/bounty.txt | python ../src/scripts/qrels2trec.py > qrels_trec.txt

../src/trec_eval/trec_eval qrels_trec.txt results_bounty_trec.txt

cat results_bounty_trec.txt | python ../src/scripts/plot_pr.py --qrels qrels_trec.txt --output prec_rec_bounty.png
