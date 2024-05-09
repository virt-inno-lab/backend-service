import yandex.cloud.iam.v1.yandex_passport_user_account_service_pb2_grpc as stub_
import yandex.cloud.iam.v1.yandex_passport_user_account_service_pb2 as yandex_pass

import channel
import grpc._channel

from grpc import StatusCode

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


# Test
if __name__ == "__main__":
    user_account = get_user_by_email("vovasst@yandex.ru")
    user_id: str = user_account.ListFields()[0][1]
    print(user_id)
