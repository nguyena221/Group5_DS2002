# DS2002 Final Project - Cooking Data
This is a recipe processing pipeline where JSON files are uploaded to an AWS S3 bucket which triggers a lambda function to convert the json file to csv, upload the new csv file to a different S3 bucket, and log the results in a SQL database. 

## Installation / building:
This project runs on AWS services, but the lambda function must be packaged for MySQL to work.
#### To download the lambda function: 
```
cd package
zip -r ../deployment.zip .
```
Download the .zip file to your computer. Then upload the .zip file to your AWS lambda. Make sure to update the environment variables and add the trigger S3 bucket in the lambda function settings.

## Usage:


## Notes:

