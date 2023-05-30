import os
import pickle
import logging
from typing import Dict, Any, List
import csv
import boto3
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Configuration values
export_bucket: str = os.environ['export_bucket']
export_filename: str = os.environ['export_filename']
test_size: float = float(os.environ['test_size'])
n_estimators: int = int(os.environ['n_estimators'])
min_samples_split: int = int(os.environ['min_samples_split'])
min_samples_leaf: int = int(os.environ['min_samples_leaf'])
max_features: str = os.environ['max_features']
max_depth: Any = eval(os.environ['max_depth'])
bootstrap: Any = eval(os.environ['bootstrap'])

def lambda_handler(event: Dict[str, Any], context: Any) -> None:
    '''
    Lambda function handler for training a random forest classifier 
    and saving the model artifact to S3

    Args:
        event: The event data passed to the lambda function
        context: The runtime information provided by AWS Lambda
    '''
    try:
        s3_client = boto3.client('s3')
        s3_resource = boto3.resource('s3')

        bucket: str = event['bucket']
        key: str = event['key']

        local_file_path: str = '/tmp/balanced_data.csv'
        s3_client.download_file(bucket, key, local_file_path)
    except (KeyError, FileNotFoundError) as e:
        logging.error(f'An error occurred while downloading the file: {str(e)}')
        raise e

    try:
        # Read data
        with open(local_file_path, 'r') as f:
            reader = csv.reader(f)
            header: List[str] = next(reader)

            features: List[List[str]] = []
            label: List[str] = []

            for row in reader:
                features.append(row[:-1])
                label.append(row[-1])
        logging.info('Data read')
    except (FileNotFoundError, csv.Error) as e:
        logging.error(f"An error occurred while reading the data: {str(e)}")
        raise e

    try:
    # Perform train-test split
        X_train, X_test, y_train, y_test = train_test_split(features, label,
                                                            test_size=test_size,
                                                            random_state=42)

        rf = RandomForestClassifier(
            n_estimators=n_estimators,
            min_samples_split = min_samples_split,
            min_samples_leaf = min_samples_leaf,
            max_features = max_features,
            max_depth = max_depth,
            bootstrap = bootstrap
            )
        rf = rf.fit(X_train,y_train)
        logging.info('Model trained')
    except ValueError as e:
        logging.error(f"An error occurred while training the model: {str(e)}")
        raise e

    try:
        # Save the trained model
        model_artifact: bytes = pickle.dumps(rf)

        # Upload the model artifact to S3
        s3_resource.Object(export_bucket, export_filename).put(Body=model_artifact)
        logging.info('Model saved')
    except (pickle.PickleError, boto3.exceptions.S3Exception) as e:
        logging.error(f"An error occurred while saving the model: {str(e)}")
        raise e
