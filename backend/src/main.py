from dataclasses import dataclass

from fastapi import FastAPI, APIRouter, Response
from pydantic import BaseModel

from move_user import get_current_user_group, Cap, update_cap
from yapassport_management import get_user_by_email
from db_logger import log

router = APIRouter()


@router.get("/api/get_caps")
def get_cap(email: str, response: Response):
    try:
        user_id = get_user_by_email(email)
        cur_cap = get_current_user_group(user_id)
        if cur_cap is Cap.nobody:
            response.status_code = 404
            return
        elif cur_cap is Cap.ydb_auditor:
            return "ydb-auditor"
        elif cur_cap is Cap.cloud_auditor:
            return "cloud-auditor"
        else:  # cur_cap is Cap.cloud_viewer:
            return "cloud-viewer"

    except ValueError:
        response.status_code = 404
        return


@dataclass
class UpdateCapsRequestDTO:
    email: str
    reason: str
    cap: str


@router.post("/api/update_caps")
def update_caps(req: UpdateCapsRequestDTO, response: Response):
    cap_enum = Cap.nobody
    if req.cap == "ydb-auditor":
        cap_enum = Cap.ydb_auditor
    elif req.cap == "cloud-auditor":
        cap_enum = Cap.cloud_auditor
    elif req.cap == "cloud-viewer":
        cap_enum = Cap.cloud_viewer
    else:
        response.status_code = 404
        return "wrong cap name"
    update_cap(req.email, cap_enum)
    log(req.email, req.reason, req.cap)
    return "done"


api = FastAPI()
api.include_router(router)
