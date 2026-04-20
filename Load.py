#!/usr/bin/env python3
import os
import mysql.connector
import logging

DBHOST = #?????
DBUSER = #????
DBPASS = #????
DB = "recipes"

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

