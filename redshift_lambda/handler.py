import psycopg2
import sys
import os

import boto3
from dotenv import load_dotenv
load_dotenv()

def start(event, context):
    print("hello world")

    host = os.getenv("DB_HOST")
    port = int(os.getenv("DB_PORT"))
    user = os.getenv("DB_USER")
    passwd = os.getenv("DB_PASS")
    db = os.getenv("DB_NAME")
    cluster = os.getenv("DB_CLUSTER")

    try:
        client = boto3.client('redshift')
        creds = client.get_cluster_credentials(  # Lambda needs these permissions as well DataAPI permissions
            DbUser=user,
            DbName=db,
            ClusterIdentifier=cluster,
            DurationSeconds=3600) # Length of time access is granted
    except Exception as ERROR:
        print("Credentials Issue: " + str(ERROR))
        sys.exit(1)

    print('got credentials')

    try:
        conn = psycopg2.connect(
            dbname=db,
            user=user,
            password=passwd,
            port=port,
            host=host)
    except Exception as ERROR:
        print("Connection Issue: " + str(ERROR))
        sys.exit(1)

    print('connected')
    
    try:
        cursor = conn.cursor()
        cursor.execute("create table test_table (id int)")
        cursor.close()
        conn.commit()
        conn.close()
    except Exception as ERROR:
        print("Execution Issue: " + str(ERROR))
        sys.exit(1)

    print('executed statement')

    # con = psycopg2.connect(
    #     "dbname=dev host=redshift-cluster-1.cduzkj2qjmlq.eu-west-2.redshift.amazonaws.com port=5439 user=test password=Password1")

