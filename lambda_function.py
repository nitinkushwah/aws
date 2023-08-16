import pymysql
import logging
import os
import json

# required Role permission: AWSLambdaVPCAccessExecutionRole
#https://repost.aws/knowledge-center/lambda-rds-connection-timeouts

"""
Create DB Manually and insert some test values
CREATE DATABASE ExampleDB;
USE ExampleDB;
CREATE TABLE Transactions (
	transaction_id INT PRIMARY KEY,
	amount DECIMAL(13,2) NOT NULL,
	transaction_type ENUM('PURCHASE', 'REFUND') NOT NULL
)

desc Transactions;


USE ExampleDB;
desc Transactions;
INSERT into Transactions (transaction_id, amount, transaction_type) values
(111, 10, 'PRUCHASE'),
(222, 200, 'REFUND');

SELECT * FROM Transactions;
"""

#Configuration Values

def get_database_connection():
    connection = pymysql.connect(
        host=os.environ['DB_HOST'],
        user=os.environ['DB_USER'],
        passwd=os.environ['DB_PASSWORD'],
        db=os.environ['DB_NAME']
    )
    return connection


logger = logging.getLogger()
logger.setLevel(logging.INFO)

connection = get_database_connection()
cursor = connection.cursor()
    
def lambda_handler(event, context): 
#Connection

#table exist
    cursor.execute('SELECT * from Transactions')
    rows = cursor.fetchall()
    row_data=[]
    for row in rows:
        row_data.append({
        'transaction_id' : row[0],
        'amount' : row[1],
        'transaction_type' : [2]
        })
        json_data=json.dumps(row_data, default=str)
        cursor.close()
        connection.close()
        return {
            'statusCode' : 200,
            'body' : json.dumps(json_data, default=str)
        }
