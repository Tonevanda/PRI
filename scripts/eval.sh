python3 ../src/scripts/query_solr.py --query queries/query_diable_jambe.json --uri http://localhost:8983/solr --collection episodes | \
python3 ../src/scripts/solr2trec.py > results_sys1_trec.txt

cat ../qrels/diable_jambe.txt | python3 ../src/scripts/qrels2trec.py > qrels_trec.txt

../src/trec_eval/trec_eval qrels_trec.txt results_sys1_trec.txt

cat results_sys1_trec.txt | python3 ../src/scripts/plot_pr.py --qrels qrels_trec.txt --output prec_rec_sys1.png
