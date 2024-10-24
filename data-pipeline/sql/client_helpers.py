import os
from google.oauth2 import service_account
from google.cloud.bigquery import Client


def get_bigquery_client(credentials_path_env_variable: str) -> Client:
    """
    Create a BigQuery client using service account credentials

    Args:
        credentials_path_env_variable: Name of env variable that stores path to service account JSON file

    Returns:
        BigQuery Client instance
    """
    service_account_json = os.getenv(credentials_path_env_variable)
    if service_account_json is None:
        raise ValueError(
            "PLINY_BIGQUERY_SERVICE_ACCOUNT environment variable is not set."
        )

    credentials = service_account.Credentials.from_service_account_file(
        service_account_json,
        scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )

    return Client(credentials=credentials, project=credentials.project_id)
