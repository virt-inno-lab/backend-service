from grpc import StatusCode
import yandex.cloud.iam.v1.yandex_passport_user_account_service_pb2_grpc as stub_
import yandex.cloud.iam.v1.yandex_passport_user_account_service_pb2 as yandex_pass

import channel
import grpc._channel

ch = channel.create_client_channel()
stub = stub_.YandexPassportUserAccountServiceStub(ch)

def get_user_by_email(email: str):
    req = yandex_pass.GetUserAccountByLoginRequest(login=email)

    try:
        user = stub.GetByLogin(req)
        return user
    except grpc._channel._InactiveRpcError as error:
        if error.code() == grpc.StatusCode.NOT_FOUND:
            raise ValueError("No such user!")
        else:
            print(f"Received unknown RPC error: code={error.code()} message={error.details()}")
