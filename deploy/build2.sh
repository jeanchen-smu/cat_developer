mkdir lambda
mkdir lambda/config
mkdir lambda/database
mkdir lambda/provider
mkdir lambda/enrich
mkdir lambda/utils

touch lambda/__init__.py

cp ./lambda/__init__.py ./lambda/config/ 
cp ../config/config_helper.py ./lambda/config/
cp ../config/config.yaml ./lambda/config/

cp ./lambda/__init__.py ./lambda/database/ 
cp ../database/position_table.py ./lambda/database/
cp ../database/vehicle_table.py ./lambda/database/
cp ../database/base_table.py ./lambda/database/

cp ./lambda/__init__.py ./lambda/provider/
cp ../provider/data_helper.py ./lambda/provider/

cp ./lambda/__init__.py ./lambda/enrich/
cp ../enrich/enrich_helper.py ./lambda/enrich/

cp ./lambda/__init__.py ./lambda/utils/
cp ../utils/time_helper.py ./lambda/utils/

cp ../downloader/lambda_position.py ./lambda/

pip install -r requirements.txt -t lambda

cd lambda
zip -r lambda.zip *.*
