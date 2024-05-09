import yandex.cloud.iam.v1.user_account_service_pb2_grpc as stub_s
import yandex.cloud.iam.v1.user_account_service_pb2 as user_acc

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

bozhinoski = "bozhinoski@yandex.ru"
vova = "vovasst@yandex.ru"

user = yapassport_management.get_user_by_email(bozhinoski)

print(
    user.id,
    user.yandex_passport_user_account,
)
