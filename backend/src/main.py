import user_account_service_pb2_grpc as stub_s
import user_account_service_pb2 as user_acc

import channel

import yapassport_management

ch = channel.create_client_channel()

user_accound_id = "ajefmmfid6p5cssshaqm" # Vova user account
req = user_acc.GetUserAccountRequest(user_account_id=user_accound_id)

stub = stub_s.UserAccountServiceStub(ch)

user = stub.Get(req)
print(
    user.id,
    user.yandex_passport_user_account,
)

user = yapassport_management.get_user_by_email("vovasst@yandex.ru")
print(
    user.id,
    user.yandex_passport_user_account,
)
