#! /bin/sh

cd /data/www/SGDBackend-NEX2/current
# elasticsearch 7 variant viewer data script
source /data/envs/sgd3/bin/activate && source prod_variables.sh && python scripts/search/index_variant_data.py
