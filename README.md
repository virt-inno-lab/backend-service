# Virtualization lab inno

## Installation

1. Install the client requirements, run the following:
```sh
python -m venv env
env/bin/python -m pip install -r requirements.txt
```
1. Run the proto compilation
```sh
make
```
If you see the similar output, then everything is allright:
```sh
user$ make
env/bin/python -m grpc_tools.protoc -I ./cloudapi/ -I ./cloudapi/third_party/googleapis/ --proto_path=./cloudapi/yandex/cloud/iam/v1/ --python_out="./src/" \
        --grpc_python_out="./src/" --pyi_out="./src/" user_account_service.proto
env/bin/python -m grpc_tools.protoc -I ./cloudapi/ -I ./cloudapi/third_party/googleapis/ --proto_path=./cloudapi/yandex/cloud/iam/v1/ --python_out="./src/" \
        --grpc_python_out="./src/" --pyi_out="./src/" user_account.proto
```

1. To clean afterwards, run `make clean`

## Usage
To run the service, execute the following command:
```sh
env/bin/python ./backend/main.py
```

## Authentication via Yandex IAM
Servise requires the Yandex IAM user token for authentication, to obtain the token, please follow the instructions [here](https://yandex.cloud/en/docs/iam/api-ref/authentication)

NB: if you have already configured the `yc` [tool](https://yandex.cloud/en/docs/cli/quickstart#install), then you can simply run the followingL
```sh
IAM_TOKEN=`yc iam create-token`
```

