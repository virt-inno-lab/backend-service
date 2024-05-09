import grpc
import os

iam_token = os.environ["IAM_TOKEN"]

api_url = "iam.api.cloud.yandex.net:443"

def create_client_channel(api_url: str = api_url, token: str = iam_token) -> grpc.Channel:
    # Call credential object will be invoked for every single RPC
    call_credentials = grpc.access_token_call_credentials(token)
    channel_credential = grpc.ssl_channel_credentials()
    # Combining channel credentials and call credentials together
    composite_credentials = grpc.composite_channel_credentials(
        channel_credential,
        call_credentials,
    )
    channel = grpc.secure_channel(api_url, composite_credentials)
    return channel
