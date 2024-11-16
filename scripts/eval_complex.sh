# Eval bounty

python ../src/scripts/query_solr.py --query queries/bounty.json --uri http://localhost:8983/solr --collection episodes | \
python ../src/scripts/solr2trec.py > ./results/results_bounty_trec.txt

cat ../qrels/bounty.txt | python ../src/scripts/qrels2trec.py > ./results/qrels_trec.txt

../src/trec_eval/trec_eval ./results/qrels_trec.txt ./results/results_bounty_trec.txt

cat ./results/results_bounty_trec.txt | python ../src/scripts/plot_pr.py --qrels ./results/qrels_trec.txt --output ./results/prec_rec_bounty.png

# Eval straw hats childhood

python ../src/scripts/query_solr.py --query queries/straw_hats_childhood.json --uri http://localhost:8983/solr --collection episodes | \
python ../src/scripts/solr2trec.py > ./results/results_shc_trec.txt

cat ../qrels/straw_hats_childhood.txt | python ../src/scripts/qrels2trec.py > ./results/qrels_trec.txt

../src/trec_eval/trec_eval ./results/qrels_trec.txt ./results/results_shc_trec.txt

cat ./results/results_shc_trec.txt | python ../src/scripts/plot_pr.py --qrels ./results/qrels_trec.txt --output ./results/prec_rec_shc.png 

# Eval ancient weapon

python ../src/scripts/query_solr.py --query queries/ancient_weapon.json --uri http://localhost:8983/solr --collection episodes | \
python ../src/scripts/solr2trec.py > ./results/results_aw_trec.txt

cat ../qrels/ancient_weapon.txt | python ../src/scripts/qrels2trec.py > ./results/qrels_trec.txt

../src/trec_eval/trec_eval ./results/qrels_trec.txt ./results/results_aw_trec.txt

cat ./results/results_aw_trec.txt | python ../src/scripts/plot_pr.py --qrels ./results/qrels_trec.txt --output ./results/prec_rec_aw.png