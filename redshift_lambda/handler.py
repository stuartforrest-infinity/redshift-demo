import psycopg2
import sys
import os

import boto3
from dotenv import load_dotenv
load_dotenv()


def start(event, context):

    host = os.getenv("DB_HOST")
    port = int(os.getenv("DB_PORT"))
    user = os.getenv("DB_USER")
    passwd = os.getenv("DB_PASS")
    db = os.getenv("DB_NAME")

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
