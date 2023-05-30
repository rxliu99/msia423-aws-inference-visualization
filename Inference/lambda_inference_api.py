import json
import boto3
import pickle
import os
import logging
from typing import Any, Dict

# Setup the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Declare a global variable to store the cached model
cached_model = None

def load_model_from_s3(s3_bucket_name: str, s3_key: str) -> Any:
    """
    Load the model object from S3.

    Args:
        s3_bucket_name (str): The name of the S3 bucket.
        s3_key (str): The key of the model object in S3.

    Returns:
        Any: The loaded model object.
    """
    s3 = boto3.client("s3")
    response = s3.get_object(Bucket=s3_bucket_name, Key=s3_key)
    model_data = response['Body'].read()
    return pickle.loads(model_data)

def initialize_model():
    """
    Initialize the model by loading it from S3 if not already cached.
    """
    global cached_model

    if cached_model is None:
        try:
            s3_bucket_name = os.environ['s3_bucket_name']
            s3_key = os.environ['s3_key']

            logger.info(f"Bucket name: {s3_bucket_name}, Key: {s3_key}")

            # Load the model object from S3
            cached_model = load_model_from_s3(s3_bucket_name, s3_key)

        except Exception as e:
            logger.error(f"Error occurred while loading the model: {e}")
            raise e

def make_prediction(model: Any, input_data: Any) -> Any:
    """
    Make predictions using the model.

    Args:
        model (Any): The loaded model object.
        input_data (Any): The input data for making predictions.

    Returns:
        Any: The prediction result.
    """
    return model.predict(input_data)

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Lambda function for making predictions using a pre-trained model.

    Args:
        event (Dict[str, Any]): The event data passed to the Lambda function.
        context (Any): The runtime information provided by AWS Lambda.

    Returns:
        Dict[str, Any]: The response object containing the prediction result.
    """
    try:
        # Initialize the model if not already cached
        initialize_model()

        # Read user input
        patient_bmi = float(event["queryStringParameters"]["bmi"])
        patient_score = float(event["queryStringParameters"]["score"])
        patient_smoke = int(event["queryStringParameters"]["smoke"])
        patient_stroke = int(event["queryStringParameters"]["stoke"])
        patient_sex = int(event["queryStringParameters"]["sex"])
        patient_age = int(float(event["queryStringParameters"]["age"]))
        patient_diabetic = int(event["queryStringParameters"]["diabetic"])
        patient_kidney = int(event["queryStringParameters"]["kidney"])

        logger.info(f"Patient information: bmi={patient_bmi}, score={patient_score}, smoke={patient_smoke}, stroke={patient_stroke}, sex={patient_sex}, age={patient_age}, diabetic={patient_diabetic}, kidney={patient_kidney}")

    except Exception as e:
        logger.error(f"Error occurred while reading event input: {e}")
        responseObject = {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)})
        }
        return responseObject

    input_data = [[patient_bmi, patient_smoke, patient_stroke, patient_score, patient_sex, patient_age, patient_diabetic, patient_kidney]]
    
    try:
        # Make a prediction using the cached model
        prediction = make_prediction(cached_model, input_data)
        predicted_class = prediction[0]

        probability = cached_model.predict_proba(input_data)[0][int(prediction[0])]

        logger.info(f"Prediction: {prediction}")

        patient_response = {
            "User info": "Here is your user information:",
            "Prediction": predicted_class,
            "Probability": probability
        }

        responseObject = {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(patient_response)
        }

        return responseObject

    except Exception as e:
        logger.error(f"Error occurred while making a prediction: {e}")
        responseObject = {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)})
        }
        return responseObject

