import json
import os
import logging
from typing import Dict, Any, List
import boto3
import botocore
import pandas as pd
from io import StringIO
from imblearn.over_sampling import SMOTE

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Configuration values
EDA_FILE= os.getenv("EDA_FILE", "for_EDA.csv")
DESTINATION_BUCKET = os.getenv("DESTINATION_BUCKET", \
                               "team10-processed-med-data")
UPSAMPLED_FILE = os.getenv("UPSAMPLED_FILE", 'balanced_data.csv')
TARGET_COL = os.getenv("TARGET_COL", "HeartDisease")

def lambda_handler(event: Dict[str, Any], context: Any) -> None:
    '''
    Lambda function handler for Data Preprocesssing

    Args:
        event: The event data passed to the lambda function
        context: The runtime information provided by AWS Lambda
    '''
    logger.info("New files uploaded to the source bucket.")
    s3_client = boto3.client('s3')
    try:
        # read data from s3
        bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
        s3_file_name = event["Records"][0]["s3"]["object"]["key"]
        obj = s3_client.get_object(Bucket=bucket_name, Key= s3_file_name)

        #process data
        logger.info("Get new file.")
        data = pd.read_csv(obj['Body'], sep=',')
        data = create_dataset(data)

        #put to another s3 bucket
        csv_buffer = StringIO()
        data.to_csv(csv_buffer, index=False)
        s3_resource = boto3.resource('s3')
        s3_resource.Object(DESTINATION_BUCKET, EDA_FILE) \
            .put(Body=csv_buffer.getvalue())
        logger.info("Put new file.")
    except KeyError as e:
        logger.error(f"KeyError: {str(e)}")
        raise e
    except FileNotFoundError as e:
        logger.error(f"FileNotFoundError: {str(e)}")
        raise e
    except pd.errors.EmptyDataError as e:
        logger.error(f"EmptyDataError: {str(e)}")
        raise e
    except botocore.exceptions.ClientError as e:
        logger.error(f"ClientError: {str(e)}")
    
    try:
        # Upsample the dataset
        x_all = data.drop(TARGET_COL, axis=1)
        y_all = data[TARGET_COL]
        # Perform oversampling using SMOTE
        smote = SMOTE()
        x_oversampled, y_oversampled = smote.fit_resample(x_all, y_all)
        # Create a new balanced dataframe
        balanced_data = pd.concat([x_oversampled, y_oversampled], axis=1)

        #upload the upsampled dataset to s3
        csv_buffer = StringIO()
        balanced_data.to_csv(csv_buffer, index=False)
        s3_resource.Object(DESTINATION_BUCKET, UPSAMPLED_FILE) \
            .put(Body=csv_buffer.getvalue())
        logger.info("Put new file.")
    except KeyError as e:
        logger.error(f"KeyError: {str(e)}")
        raise e
    except FileNotFoundError as e:
        logger.error(f"FileNotFoundError: {str(e)}")
        raise e
    except pd.errors.EmptyDataError as e:
        logger.error(f"EmptyDataError: {str(e)}")
        raise e


def create_dataset(data: pd.DataFrame) -> pd.DataFrame:
    """Creates dataset from specified data path

    Args:
        data:pandas dataframe
    
    Returns:
        Pandas dataframe for data
    """
    logger.info("Create Dataset in process")

    columns = ["BMI", "Smoking", "Stroke", "PhysicalHealth", \
               "Sex", "Age","Diabetic", "KidneyDisease", "HeartDisease"]
    cat_cols = ["Smoking", "Stroke", "KidneyDisease", "HeartDisease"]

    logger.warning("Make sure the data is correctly formatted")
    # Convert to binary
    for col in cat_cols:
        data[col] = (data[col]=="Yes").astype(int)

    # Map Aging to its categories
    def age_mapping(ages):
        return int(ages[:2])
    data["AgeCategory"] = data["AgeCategory"].apply(age_mapping)
    data.rename(columns={"AgeCategory": "Age"}, inplace=True)

    # Map diabetic to its categories
    def diabetic_mapping(answer):
        return int(answer[:2]=="Ye")
    data["Diabetic"] = data["Diabetic"].apply(diabetic_mapping)

    # Female:1, Male:0
    data["Sex"] = (data["Sex"]=="Female").astype(int)

    data = data[columns]
    logger.info("Dataset created")

    return data
