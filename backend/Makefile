BACKEND=

BACKEND += ./src/user_account_service_pb2.py
BACKEND += ./src/user_account_service_pb2.pyi
BACKEND += ./src/user_account_service_pb2_grpc.py

BACKEND += ./src/user_account_pb2.py
BACKEND += ./src/user_account_pb2.pyi
BACKEND += ./src/user_account_pb2_grpc.py

BACKEND += ./src/yandex_passport_user_account_service_pb2.py
BACKEND += ./src/yandex_passport_user_account_service_pb2.pyi
BACKEND += ./src/yandex_passport_user_account_service_pb2_grpc.py

ARTIFACTS=

ARTIFACTS += ./src/user_account_service_pb2.py
ARTIFACTS += ./src/user_account_service_pb2.pyi
ARTIFACTS += ./src/user_account_service_pb2_grpc.py

ARTIFACTS += ./src/user_account_pb2.py
ARTIFACTS += ./src/user_account_pb2.pyi
ARTIFACTS += ./src/user_account_pb2_grpc.py

ARTIFACTS += ./src/yandex_passport_user_account_service_pb2.py
ARTIFACTS += ./src/yandex_passport_user_account_service_pb2.pyi
ARTIFACTS += ./src/yandex_passport_user_account_service_pb2_grpc.py

GEN_PATH="./src/"

.PHONY: all
all: ${ARTIFACTS}

./src/user_account_service_pb2.py ./src/user_account_service_pb2.pyi ./src/user_account_service_pb2_grpc.py:
	env/bin/python -m grpc_tools.protoc -I ./cloudapi/ -I ./cloudapi/third_party/googleapis/ --proto_path=./cloudapi/yandex/cloud/iam/v1/ --python_out=${GEN_PATH} \
    	--grpc_python_out=${GEN_PATH} --pyi_out=${GEN_PATH} user_account_service.proto

./src/user_account_pb2.py ./src/user_account_pb2.pyi ./src/user_account_pb2_grpc.py:
	env/bin/python -m grpc_tools.protoc -I ./cloudapi/ -I ./cloudapi/third_party/googleapis/ --proto_path=./cloudapi/yandex/cloud/iam/v1/ --python_out=${GEN_PATH} \
    	--grpc_python_out=${GEN_PATH} --pyi_out=${GEN_PATH} user_account.proto

./src/yandex_passport_user_account_service_pb2.py ./src/yandex_passport_user_account_service_pb2.pyi ./src/yandex_passport_user_account_service_pb2_grpc.py:
	env/bin/python -m grpc_tools.protoc -I ./cloudapi/ -I ./cloudapi/third_party/googleapis/ --proto_path=./cloudapi/yandex/cloud/iam/v1/ --python_out=${GEN_PATH} \
    	--grpc_python_out=${GEN_PATH} --pyi_out=${GEN_PATH} yandex_passport_user_account_service.proto

.PHONY: backend
backend: ${BACKEND}

.PHONY: clean
clean:
	rm -f ${ARTIFACTS}
	rm -rf __pycache__
