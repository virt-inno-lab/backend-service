# Virtualization lab inno

## Installation

1. Install the client requirements, run the following:
 ```sh
 python -m venv env
 source env/bin/activate
 env/bin/python -m pip install -r requirements.txt
 ```

## Usage
To run the service, execute the following command:
```sh
env/bin/python ./backend/main.py
```

## Authentication via Yandex IAM
Service requires the Yandex IAM user token for authentication, to obtain the token, please follow the instructions [here](https://yandex.cloud/en/docs/iam/api-ref/authentication)

NB: if you have already configured the `yc` [tool](https://yandex.cloud/en/docs/cli/quickstart#install), then you can simply run the following:
```sh
IAM_TOKEN=`yc iam create-token`
```

