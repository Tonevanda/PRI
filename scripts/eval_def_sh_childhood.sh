python ../src/scripts/query_solr.py --query queries/def_straw_hats_childhood.json --uri http://localhost:8983/solr --collection episodes | \
python ../src/scripts/solr2trec.py > ./results/results_def_sh_childhood_trec.txt

cat ../qrels/straw_hats_childhood.txt | python ../src/scripts/qrels2trec.py > ./results/qrels_trec.txt

../src/trec_eval/trec_eval ./results/qrels_trec.txt ./results/results_def_sh_childhood_trec.txt

cat ./results/results_def_sh_childhood_trec.txt | python ../src/scripts/plot_pr.py --qrels ./results/qrels_trec.txt --output ./results/prec_rec_def_childhood.png