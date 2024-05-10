import boto3
import os
import datetime
import json

LOGGING_SECRET_KEY = os.environ["LOGGING_SECRET_KEY"]
LOGGING_SECRET_KEY_ID = os.environ["LOGGING_SECRET_KEY_ID"]



def log(email, reason, new_cap):
    client = boto3.client('kinesis',
                          endpoint_url="https://yds.serverless.yandexcloud.net",
                          region_name="ru-central-1",
                          aws_access_key_id=LOGGING_SECRET_KEY_ID,
                          aws_secret_access_key=LOGGING_SECRET_KEY)

    log_entry_json = {
        "email": email,
        "new_cap": new_cap,
        "reason": reason
    }

    client.put_record(
        StreamName="/ru-central1/b1giekpmcv3no5p0g1d9/etnsro03ueudc94alh8o/log-stream",
        Data=json.dumps(log_entry_json), PartitionKey="escalation-log")

log(email="a@example.com", reason="i want to die", new_cap="cloud.viewer")
