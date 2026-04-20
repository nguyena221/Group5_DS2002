#!/usr/bin/env python3
import os
import mysql.connector
import logging

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

        file_id = cursor.lastrowid
        logging.info(f"Inserted file with ID: {file_id}")
        cursor.close()
        db.close()
    except Exception as e:
        logging.error(f"File insert failed: {str(e)}")

def lambda_handler(event, context):
    input_key = ""
    output_key = ""
    input_bucket = ""
    output_bucket = ""
    try:
        record = event['Records'][0]
        input_bucket = record['s3']['bucket']['name']
        input_key = record['s3']['object']['key']

        output_key = input_key.replace(".json",".csv")
        output_bucket = "cooking-output"

        log_to_recipes(input_key, output_key, input_bucket, output_bucket, "SUCCESS")
    
    except Exception as e:
        log_to_recipes(input_key, output_key, input_bucket, output_bucket, "FAILED")

