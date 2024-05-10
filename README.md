# Virtualization lab inno

## https://iam-service.ddns.net/

## Description
This is a simple implementation of the Identity Access Management (IAM) system
within the context of the Yandex Cloud for the Total Virtualization course of
Innopolis University Spring 2024 semester.

The goal of the service is simple: to provide the user the ability to request
the elevation of the privileges through the cloud management tools. We have
developed three distinct groups with different privilege set.
1. asmnt-ydb-auditor    - group that can audit only the YDB resource
2. asmnt-cloud-auditor  - group that can audit the whole cloud
3. asmnt-cloud-viewer   - group that can view the settings of the whole cloud

You can see this groups and their members here: https://org.yandex.cloud/groups

The roles described above are given in the order of [increasing
capabilities](https://yandex.cloud/en/docs/iam/roles-reference), so the latter
role includes all the capabilites of the previous one.

## Implementation
The implementation is rather simple. We have developed the backend service with
Fastapi, cool and easy to work with python library. Fastapi serves static html
files, which contain simple user form. User then fills the form to elevate the
privileges. Then several gRPC calls are made to the public API of the Yandex 
Cloud, thus handling the user group management.

The user management is done via the special type of the account called
**service accounts**. In our implementation we have two service accounts: one
for group management, the other one is for logging only. These service accounts
have limited roles, so in case of token leak or something else, we reduce the
blast radius.

### Logging
Logging is implemented using [Yandex Data Stream](https://yandex.cloud/en/docs/data-streams/concepts/glossary?utm_source=console&utm_medium=help-center&utm_campaign=data-streams)
service, which is simple to use and simple to integrate into the production 
environment. It uses boto3 as a client and Yandex Cloud managed kinesis 
installation to ingest logs.

## Installation

### Backend requirements installation
- Install the client requirements, run the following:
```shell
cd backend
python -m venv env
source env/bin/activate
env/bin/python -m pip install -r requirements.txt
```

### Frontend requirements installation
- Install npm
- Run the following:
```shell
cd frontend
npm i
```


## Docker build and run
To run the service, execute the following command:
```shell
docker build -t iam .
docker run -p 127.0.0.1:8000:80 -v <authorized_key_json_path>:/app/auth_key.json:ro -e AUTH_TOKEN_PATH=/app/auth_key.json -e LOGGING_SECRET_KEY=<LOGGING_SECRET_KEY> -e LOGGING_SECRET_KEY_ID=<LOGGING_SECRET_KEY_ID> -d iam
```

And check your service at http://127.0.0.1:8000

## Configuration

### Service account authentication
To run the server, you need to configure the access tokens for the service
accounts, this can be done via [this guide](https://yandex.cloud/en/docs/iam/quickstart-sa). 

Note that you need to get the `authorized_key.json` file. This is crucial,
because the Yandex IAM token is alive only for 12 hours and if you need your
service to be up and running 24/7, we have implemented the authomatic IAM token
request, this is done using the `authorized_key.json` file.

Then set the variable `AUTH_TOKEN_PATH` as the absolute path for the
`authorized_key.json` file. **NB: check the permissions for the aforementioned
file!**

### Logging authentication

The variables `LOGGING_SECRET_KEY` and `LOGGING_SECRET_KEY_ID` represent the S3
logging service account credentials and are essential for the logging.

## License
Licensed to MIT OpenSource License 2024, the iam-service team.
