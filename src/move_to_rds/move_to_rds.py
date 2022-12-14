import sys
import os
import logging
import pymysql
import boto3
import pandas as pd
from sqlalchemy import create_engine

#rds settings
rds_host  = os.environ['RDS_HOST']
name = os.environ['USERNAME']
password = os.environ['PASSWORD']
db_name = os.environ['DB_NAME']

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    conn = pymysql.connect(host=rds_host, user=name, password=password, db=db_name, connect_timeout=5)
except pymysql.MySQLError as e:
    logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
    logger.error(e)
    sys.exit()

logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")
def handler(event, context):
    """
    This function fetches content from MySQL RDS instance
    """

    bucket_name = event['Records'][0]['s3']['bucket']['name']
    key_name = event['Records'][0]['s3']['object']['key']

    s3 = boto3.client("s3")

    file_content = s3.get_object(
        Bucket=bucket_name, Key=key_name)["Body"]

    df = pd.read_csv(file_content)

    engine = create_engine("mysql+mysqlconnector://{user}:{pw}@{host}/{db}".format(user=name, pw=password, host=rds_host, db=db_name))

    with conn.cursor() as cur:
        cur.execute("create table IF NOT EXISTS NewsStories(title varchar(255) NOT NULL, description varchar(255), author varchar(255), date varchar(255), link varchar(255) NOT NULL, source varchar(255) NOT NULL, created_date varchar(255) NOT NULL, PRIMARY KEY (link))")
        df.to_sql(con=engine, name='NewsStories', if_exists='append', index=False)
        conn.commit()
        cur.execute("select * from NewsStories")
        for row in cur:
            print(row)
    conn.commit()
