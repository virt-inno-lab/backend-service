import json
import time
import grpc
import os

import jwt
import requests

iam_token = ""
last_renewed_time = 0.0

auth_token_path = os.environ["AUTH_TOKEN_PATH"]

api_url = "iam.api.cloud.yandex.net:443"


def renew_token():
    global iam_token, last_renewed_time
    if last_renewed_time + 3600.0 < time.time():
        with open(auth_token_path, "r") as auth_token_file:
            auth_token = json.load(auth_token_file)
            service_account_id = auth_token["service_account_id"]
            key_id = auth_token["id"]
            private_key = auth_token["private_key"]

            now = int(time.time())
            payload = {
                'aud': 'https://iam.api.cloud.yandex.net/iam/v1/tokens',
                'iss': service_account_id,
                'iat': now,
                'exp': now + 360}

            # JWT generation.
            encoded_token = jwt.encode(
                payload,
                private_key,
                algorithm='PS256',
                headers={'kid': key_id})
            resp = requests.post("https://iam.api.cloud.yandex.net/iam/v1/tokens", json={"jwt": encoded_token})
            iam_token = resp.json()["iamToken"]
            last_renewed_time = time.time()


def create_client_channel(api_url: str = api_url) -> grpc.Channel:
    renew_token()
    # Call credential object will be invoked for every single RPC
    call_credentials = grpc.access_token_call_credentials(iam_token)
    channel_credential = grpc.ssl_channel_credentials()
    # Combining channel credentials and call credentials together
    composite_credentials = grpc.composite_channel_credentials(
        channel_credential,
        call_credentials,
    )
    channel = grpc.secure_channel(api_url, composite_credentials)
    return channel
