import boto3

client = boto3.client("lambda")

client.update_function_code(
    FunctionName='cron-job-data-getter',
    S3Bucket='news-artifacts-kvh',
    S3Key='cron-data-getter/data_getter.zip'
)

client.update_function_code(
    FunctionName='moveNewsToRDS',
    S3Bucket='news-artifacts-kvh',
    S3Key='cron-data-getter/move_rds.zip'
)