#!/usr/bin/env python3
import os
import mysql.connector
import logging
import boto3
import json
import urllib.parse
from converting_logic import convert_json_to_csv

DBHOST = os.environ['DB_HOST']
DBUSER = os.environ['DB_USER']
DBPASS = os.environ['DB_PASS']
DB = os.environ['DB_NAME']


def log_to_recipes(input_key, output_key, input_bucket, output_bucket, status):
    try:
        db = mysql.connector.connect(host=DBHOST, user=DBUSER, password=DBPASS, database=DB)
        cursor = db.cursor()
        query = "INSERT INTO file_processing_log (input_key, output_key, input_bucket, output_bucket, status) VALUES (%s, %s, %s, %s, %s)"
        insert_data = (input_key, output_key, input_bucket, output_bucket, status)
        cursor.execute(query, insert_data)
        db.commit()
        cursor.close()
        db.close()
    except Exception as e:
        logging.error(str(e))


def lambda_handler(event, context):
    record = event['Records'][0]
    input_bucket = record['s3']['bucket']['name']
    input_key = urllib.parse.unquote_plus(event["Records"][0]["s3"]["object"]["key"], encoding="utf-8")

    output_bucket = os.environ['OUTPUT_BUCKET']
    output_key = input_key.replace(".json", ".csv")

    if input_bucket == os.environ['OUTPUT_BUCKET']:
        print("Source and destination buckets are the same. Aborting file transformation operation.")
        return
    if input_key.endswith(".csv"):
        print("Input file not json format. Aborting file transformation.")
        return

    try:
        s3 = boto3.client('s3')

        response = s3.get_object(Bucket=input_bucket, Key=input_key)
        file_content = response['Body'].read().decode('utf-8')

        json_data = json.loads(file_content)
        csv_output = convert_json_to_csv(json_data)
    
        s3.put_object(
            Bucket=output_bucket,
            Key=output_key,
            Body=csv_output
        )
        print(f"Transforming {input_key} from {input_bucket} to {output_bucket}.")

        log_to_recipes(input_key, output_key, input_bucket, output_bucket, "SUCCESS")

    except Exception as e:
        logging.error(str(e))
        log_to_recipes(input_key, output_key, input_bucket, output_bucket, "FAILED")
