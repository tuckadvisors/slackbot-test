from datetime import datetime
import json
import urllib.parse
import logging

from flask import Flask
from flask_restx import Api, Resource

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


app = Flask(__name__)
api = Api(app, version='1.0', title='DateTime API',
          description='A simple API to get current date and time')

ns = api.namespace(
    'datetime', description='Operations related to date and time')


@ns.route('/')
class DateTimeResource(Resource):
    @ns.doc('get_date_time')
    def get(self):
        """Fetch the current date and time"""

        secret_name = "Tuck_Advisors_Slackbot_Token"
        region_name = "us-east-1"
        secret_value = get_secret(secret_name, region_name)
        # print(secret_value['SecretString'])
        # secret_dict = json.loads(secret_value['SecretString'])
        # print(secret_dict)
        # print(secret_dict['slacktoken'])

        logger.log(
            logging.INFO, f"Retrieved secret value from AWS Secrets Manager: ({secret_name}, {secret_value})")

        current_time = datetime.now().isoformat()
        return {'current_date_time': current_time}


if __name__ == '__main__':
    app.run(debug=True)
