import user_account_service_pb2_grpc as stub_s
import user_account_service_pb2 as user_acc

import grpc
import os

token = os.environ["IAM_TOKEN"]

api_url = "iam.api.cloud.yandex.net:443"

def create_client_channel(addr: str, token: str) -> grpc.Channel:
    # Call credential object will be invoked for every single RPC
    call_credentials = grpc.access_token_call_credentials(token)
    channel_credential = grpc.ssl_channel_credentials()
    # Combining channel credentials and call credentials together
    composite_credentials = grpc.composite_channel_credentials(
        channel_credential,
        call_credentials,
    )
    channel = grpc.secure_channel(addr, composite_credentials)
    return channel


channel = create_client_channel(api_url, token)

user_accound_id = "ajefmmfid6p5cssshaqm" # Vova user account
req = user_acc.GetUserAccountRequest(user_account_id=user_accound_id)

stub = stub_s.UserAccountServiceStub(channel)

a = stub.Get(req)
