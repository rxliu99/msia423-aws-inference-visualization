import json
import os
import logging
from typing import Dict, Any, List
import boto3
import pandas as pd
from matplotlib import pyplot as plt

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Configuration values
LOCAL_FILE_NAME = os.getenv("BUCKET_NAME", "for_EDA.csv")
DESTINATION_BUCKET = os.getenv("DESTINATION_BUCKET", \
                               "team10.med.data.visualization")
LOCAL_PREFIX = os.getenv("LOCAL_PREFIX", "/tmp")
LOCAL_FILE_PATH = os.path.join(LOCAL_PREFIX, LOCAL_FILE_NAME)

def lambda_handler(event: Dict[str, Any], context: Any) -> None:
    '''
    Lambda function handler for Visualizations

    Args:
        event: The event data passed to the lambda function
        context: The runtime information provided by AWS Lambda
    '''
    try:
        logger.info("New files uploaded to the source bucket.")
        bucket = event['bucket']
        key = event['key']
        # Download file from S3
        s3_client = boto3.client('s3')
        s3_client.download_file(bucket, key, LOCAL_FILE_PATH)
    except (KeyError, FileNotFoundError) as e:
        logging.error(f'An error occurred while downloading the file:\
                       {str(e)}')
        raise e

    try:
        # Read file into dataframe
        df_eda = pd.read_csv(LOCAL_FILE_PATH)
        fig_paths = save_figures(df_eda, LOCAL_PREFIX, DESTINATION_BUCKET)
        logging.info(f'Figures saved to {fig_paths}')
    except ValueError as e:
        logging.error(f'ValueError: {str(e)}')
        raise e
    except FileNotFoundError as e:
        logging.error(f'FileNotFoundError: {str(e)}')
        raise e

def save_figures(data: pd.DataFrame, directory: str, bucket_name: str) \
    -> List[str]:
    """EDA on dataset and saves generated plots to directory

    Args:
        data: dataframe to do eda
        directory: directory of resulting plots to be saved to
        bucket_name: name of s3 bucket to save plots to 

    Returns:
        a list of saved figure paths
    """
    s3_client = boto3.client('s3')
    logger.info("EDA Figure in process")
    fig_paths = []
    num_cols = ["BMI","Age","PhysicalHealth"]
    colors = ["lightcoral","lightgreen"]

    df1 = data[data["HeartDisease"] == 1]
    df2 = data[data["HeartDisease"] == 0]

    # Numerical features
    for feat in num_cols:
        logger.debug("looping through all columns")

        plt.rcParams["figure.figsize"] = [7.50, 3.50]
        plt.rcParams["figure.autolayout"] = True

        fig, axs = plt.subplots(1, 2, figsize=(10, 5))

        df1.hist(feat, ax=axs[0], color=colors[0], grid=False)
        df2.hist(feat, ax=axs[1], color=colors[1], grid=False)

        axs[0].set_title(feat + " Distribution (Heart Disease)")
        axs[1].set_title(feat + " Distribution (No Heart Disease)")

        # Save figure
        fig_path = os.path.join(directory, f"{feat}.png")
        plt.savefig(fig_path)
        s3_client.upload_file(fig_path, bucket_name, f"{feat}.png")
        fig_paths.append(fig_path)
        logger.info("EDA Figure saved")

    # Categorical features
    cat_cols = ['Smoking', 'Stroke', 'Diabetic', 'KidneyDisease']
    for feat in cat_cols:
        category_counts_h = df1[feat].value_counts()
        category_counts_n = df2[feat].value_counts()
        category_df_h = pd.DataFrame({feat: category_counts_h.index, \
                                      'Count': category_counts_h.values})
        category_df_n = pd.DataFrame({feat: category_counts_n.index, \
                                      'Count': category_counts_n.values})

        plt.rcParams["figure.figsize"] = [7.50, 3.50]
        plt.rcParams["figure.autolayout"] = True
        fig, axs = plt.subplots(1, 2, figsize=(10, 5))

        # Plot histogram for category_df_h
        axs[0].bar(category_df_h[feat], category_df_h['Count'], color='lightblue')
        axs[0].set_ylabel('Count')
        axs[0].set_title(feat + ' Distribution (Heart Disease)')
        axs[0].set_xticks([0, 1])
        axs[0].set_xticklabels(['No', 'Yes'])

        # Plot histogram for category_df_n
        axs[1].bar(category_df_n[feat], category_df_n['Count'], color='lightblue')
        axs[1].set_ylabel('Count')
        axs[1].set_title(feat + ' Distribution (No Heart Disease)')
        axs[1].set_xticks([0, 1])
        axs[1].set_xticklabels(['No', 'Yes'])

       # Save figure
        fig_path = os.path.join(directory, f"{feat}.png")
        plt.savefig(fig_path)
        s3_client.upload_file(fig_path, bucket_name, f"{feat}.png")
        fig_paths.append(fig_path)
        logger.info("EDA Figure saved")

    ## Histogram for sex
    category_counts_h = df1['Sex'].value_counts()
    category_counts_n = df2['Sex'].value_counts()
    category_df_h = pd.DataFrame({'Sex': category_counts_h.index, \
                                  'Count': category_counts_h.values})
    category_df_n = pd.DataFrame({'Sex': category_counts_n.index, \
                                  'Count': category_counts_n.values})

    fig, axs = plt.subplots(1, 2, figsize=(10, 5))

    # Plot histogram for category_df_h
    axs[0].bar(category_df_h['Sex'], category_df_h['Count'], color='lightblue')
    axs[0].set_ylabel('Count')
    axs[0].set_title('Gender Distribution (Heart Disease)')
    axs[0].set_xticks([0, 1])
    axs[0].set_xticklabels(['Male', 'Female'])

    # Plot histogram for category_df_n
    axs[1].bar(category_df_n['Sex'], category_df_n['Count'], color='lightblue')
    axs[1].set_ylabel('Count')
    axs[1].set_title('Gender Distribution (No Heart Disease)')
    axs[1].set_xticks([0, 1])
    axs[1].set_xticklabels(['Male', 'Female'])

    # Save figure
    fig_path = os.path.join(directory, f"Sex.png")
    plt.savefig(fig_path)
    s3_client.upload_file(fig_path, bucket_name, "Sex.png")
    fig_paths.append(fig_path)
    logger.info("EDA Figure saved")

    return fig_paths
