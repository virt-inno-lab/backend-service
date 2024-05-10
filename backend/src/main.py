import os
from dataclasses import dataclass

from fastapi import FastAPI, APIRouter, Response
from starlette.staticfiles import StaticFiles

import move_user
import yapassport_management
import db_logger
from move_user import Cap

router = APIRouter()
static_resources_path = os.environ["STATIC_RESOURCES"]


@router.get("/api/get_caps")
def get_cap(email: str, response: Response):
    try:
        user_id = yapassport_management.get_user_by_email(email)
        cur_cap = move_user.get_current_user_group(user_id)
        if cur_cap is Cap.nobody:  # set role for new users
            move_user.add_cap(user_id, Cap.ydb_auditor)
            return "ydb-auditor"
        elif cur_cap is Cap.ydb_auditor:
            return "ydb-auditor"
        elif cur_cap is Cap.cloud_auditor:
            return "cloud-auditor"
        else:  # cur_cap is Cap.cloud_viewer:
            return "cloud-viewer"

    except ValueError:
        response.status_code = 404
        return "User not found"


@dataclass
class UpdateCapsRequestDTO:
    email: str
    reason: str
    cap: str


@router.post("/api/update_caps")
def update_caps(req: UpdateCapsRequestDTO, response: Response):
    try:
        user_id = yapassport_management.get_user_by_email(req.email)
        cur_cap = move_user.get_current_user_group(user_id)

        if req.cap == "ydb-auditor":
            new_cap = Cap.ydb_auditor
        elif req.cap == "cloud-auditor":
            new_cap = Cap.cloud_auditor
        elif req.cap == "cloud-viewer":
            new_cap = Cap.cloud_viewer
        else:
            response.status_code = 404
            return "wrong cap name"

        db_logger.log(req.email, req.reason, req.cap)
        if cur_cap is not Cap.nobody:
            move_user.remove_cap(user_id, cur_cap)
        move_user.add_cap(user_id, new_cap)
        return "done"

    except ValueError:
        response.status_code = 404
        return "User not found"


app = FastAPI()
app.include_router(router)
app.mount(
    "/",
    StaticFiles(directory=static_resources_path, html=True),
    name="static",
)
