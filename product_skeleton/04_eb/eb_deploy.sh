# Create application
eb init weather-cron-1344 --region us-west-2 --platform Docker --key dwoodbridge

# Create environment : Use environment variable from the system.
eb create week1-1344 --verbose --envvars AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID --envvars AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY --envvars API_KEY=$API_KEY


#aws codepipeline create-pipeline --cli-input-json file://pipeline.json
#aws codepipeline create-pipeline --cli-input-json file://pipeline_worker.json
