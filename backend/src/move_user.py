from enum import Enum
import yandex.cloud.organizationmanager.v1.group_service_pb2 as group_svc
import yandex.cloud.organizationmanager.v1.group_service_pb2_grpc as stub_s

import channel

ch = channel.create_client_channel(api_url="organization-manager.api.cloud.yandex.net:443")
stub = stub_s.GroupServiceStub(ch)

cloud_viewer_group_id = "aje8n2lo3qgvonq89vda"
cloud_auditor_group_id = "ajepvpnnbfu59fjao19q"
ydb_auditor_group_id = "ajemvl6fg8oqp4p6llmt"


class Cap(Enum):
    nobody = ""
    ydb_auditor = ydb_auditor_group_id
    cloud_auditor = cloud_auditor_group_id
    cloud_viewer = cloud_viewer_group_id


def get_current_user_group(user_id, caps=Cap) -> Cap:
    for group in caps:
        group_id = group.value
        if group == Cap.nobody:
            continue
        req = group_svc.ListGroupMembersRequest(group_id=group_id, page_size=10, page_token="")
        resp = stub.ListMembers(req)

        for member in resp.members:
            if member.subject_id == user_id:
                return group
    return Cap.nobody


def remove_cap(user_id: str, cap: Cap):
    delete_delta = group_svc.MemberDelta(action=group_svc.MemberDelta.MemberAction.REMOVE, subject_id=user_id)
    delete_req = group_svc.UpdateGroupMembersRequest(group_id=cap.value, member_deltas=[delete_delta])
    stub.UpdateMembers(delete_req)


def add_cap(user_id: str, cap: Cap):
    add_delta = group_svc.MemberDelta(action=group_svc.MemberDelta.MemberAction.ADD, subject_id=user_id)
    add_req = group_svc.UpdateGroupMembersRequest(group_id=cap.value, member_deltas=[add_delta])
    stub.UpdateMembers(add_req)
