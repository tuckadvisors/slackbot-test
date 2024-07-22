from datetime import datetime
import json
import urllib.parse
import logging

import boto3
from botocore.exceptions import ClientError

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_secret(secret_name, region_name):
    """
    Retrieves a secret value from AWS Secrets Manager service based on the secret name and region name.

    Parameters:
    secret_name (str): The name or ARN of the secret.
    region_name (str): The AWS region where the secret is stored.

    Returns:
    str: The secret value.

    Raises:
    botocore.exceptions.ClientError: If an error occurs while retrieving the secret.
    """

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
        # secret = get_secret_value_response['SecretString']
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    return secret_value_response


def lambda_handler(event, context):
    logger.info("Received event: %s", json.dumps(event))

    # Parse the incoming request from Slack
    body = event['body']
    params = urllib.parse.parse_qs(body)

    # Extract the command text (if any)
    command_text = params.get('text', [''])[0]
    logger.info(f"Command text: {command_text}")

    # look up a secret (not used)
    secret_name = "Tuck_Advisors_Slackbot_Token"
    region_name = "us-east-1"
    secret_value = get_secret(secret_name, region_name)
    secret_dict = json.loads(secret_value['SecretString'])
    slacktoken = secret_dict['slacktoken']
    slacktoken = "XXXXXXXX"
    logger.info(
        f"Retrieved secret value from AWS Secrets Manager: ({secret_name}, {slacktoken})")

    current_date_time = datetime.now().isoformat()
    logger.info(f"Current date and time: {current_date_time}")

    # Prepare the response back to Slack
    response_text = f"{current_date_time} {command_text}"
    logger.info(f"response_text:{response_text}")

    slack_response = {
        "response_type": "in_channel",
        "text": response_text
    }
    logger.info("Slack response: %s", json.dumps(slack_response))

    return {
        'statusCode': 200,
        'body': json.dumps(slack_response),
        'headers': {
            'Content-Type': 'application/json'
        }
    }
