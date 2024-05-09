import yandex_passport_user_account_service_pb2_grpc as stub_
import yandex_passport_user_account_service_pb2 as yandex_pass

import channel

ch = channel.create_client_channel()
stub = stub_.YandexPassportUserAccountServiceStub(ch)

def get_user_by_email(email: str):
    req = yandex_pass.GetUserAccountByLoginRequest(login=email)
    user = stub.GetByLogin(req)

    return user

