import boto3

client = boto3.client("lambda", region_name="us-west-1")
client.update_function_code(
    FunctionName='cron-job-data-getter',
    S3Bucket='news-artifacts-kvh',
    S3Key='cron-data-getter/lambda.zip'
)