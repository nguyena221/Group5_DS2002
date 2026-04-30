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

## 1. Access the AWS CLI on the HPC System:
Log in to the UVA HPC system via VS Code and initialize your environment to access the AWS CLI tools.
```
module load miniforge
source activate ds2002
```
## 2. Create the S3 Buckets:
Create the input bucket (where JSON files are uploaded) and the output bucket (where processed files are stored).
```
aws s3 mb s3://cooking-input
aws s3 mb s3://cooking-output
```
Note: You can verify these were created by checking the S3 section of the AWS Console.
*Note: You can verify these were created by checking the S3 section of the AWS Console.*
## 3. Create the Lambda Function:
a) Navigate to Lambda in the AWS Console and click Create function.

b) Name it cooking-data-transform and set the Runtime to Python 3.12 (or the latest available version).

c) Click Create function.

## 4. Configure the S3 Trigger:
a) Inside your function, click Add trigger.

b) Select S3 as the source.

c) Select your cooking-input bucket.

d) Set Event Type to All object create events.

e) Acknowledge the warning and click Add.

## 5. Configure Environment Variables:
a) Go to the Configuration tab > Environment variables > Edit.

b) Click Add environment variable.

c) Set Key to destination_bucket and Value to cooking-output.

d) Click Save and then click Deploy on the main function page to update the code.

## 6. Update IAM Permissions:
The Lambda needs permission to read from the input bucket and write to the output bucket.

a) Go to Configuration > Permissions and click the link under Role name.

b) Click Add permissions > Create inline policy.

c) Switch to the JSON tab and paste the following:

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowS3GetObject",
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket",
                "s3:GetObject"
            ],
            "Resource": [
                "arn:aws:s3:::cooking-input/*",
                "arn:aws:s3:::cooking-input/"
            ]
        },
        {
            "Sid": "AllowS3PutObject",
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:PutObjectAcl"
            ],
            "Resource": [
                "arn:aws:s3:::cooking-output/*"
            ]
        }
    ]
}
```
d) Click Next, name the policy s3-copy-in-out, and click Create policy.

## 7. Create and Upload a Sample Recipe:
Create a JSON file locally in VS Code. 
*Note: Simple .txt files will not work for this specific pipeline; it requires structured data.*
```
# Example of creating a JSON file manually
echo '{"recipe_id": 1, "name": "Pasta", "ingredients": ["flour", "eggs"]}' > recipe-1.json

# Upload the file to trigger the Lambda
aws s3 cp recipe-1.json s3://cooking-input
```
## 8. Verify the Results: 
a) Check the cooking-output bucket in the S3 console to see the processed file.

b) To troubleshoot, go to the Monitor tab in your Lambda function.

c) Click View CloudWatch logs and select the latest Log Stream to confirm the function initialized and successfully moved the data.

## 9. Querying the Database
Connect to MySQL.
```
module load apptainer
apptainer run ~/mysql-8.0.sif mysql -h ds2002.cgls84scuy1e.us-east-1.rds.amazonaws.com -P 3306 -u USERNAME -p PASSWORD
```
Load and Query Database.
```
USE recipes;

SELECT *
FROM recipes.file_processing_log
WHERE Status = 'SUCCESS';
```
Now you should see all of the JSON recipe files that were successfully coverted to CSV files.

## Usage:


## Notes:

