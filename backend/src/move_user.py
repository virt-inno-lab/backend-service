import yandex.cloud.organizationmanager.v1.group_service_pb2 as group_svc
import yandex.cloud.organizationmanager.v1.group_service_pb2_grpc as stub_s

import channel
import yapassport_management

ch = channel.create_client_channel(api_url="organization-manager.api.cloud.yandex.net:443")
stub = stub_s.GroupServiceStub(ch)

cloud_viewer_group_id = "aje8n2lo3qgvonq89vda"
cloud_auditor_group_id = "ajepvpnnbfu59fjao19q"
ydb_auditor_group_id = "ajemvl6fg8oqp4p6llmt"


from enum import Enum
 
class Cap(Enum):
    nobody = ""
    ydb_auditor = ydb_auditor_group_id
    cloud_auditor = cloud_auditor_group_id
    cloud_viewer = cloud_viewer_group_id


def __get_current_user_group(user_id, caps=Cap) -> Cap:
    ans = Cap.nobody
    for group in caps:
        group_id = group.value
        if group == Cap.nobody:
            continue
        req = group_svc.ListGroupMembersRequest(group_id=group_id, page_size=10, page_token="")
        resp = stub.ListMembers(req)
        
        for member in resp.members:
            if member.subject_id == user_id:
                ans = group
    
    return ans

# High level function that is called outside
def update_cap(email: str, cap: Cap):
    user = yapassport_management.get_user_by_email(email)
    
    ug = __get_current_user_group(user.id)
    if ug == Cap.nobody:
        raise ValueError("User not found!")
    
    current_user_group = ug.value
    new_user_group = cap.value

    if new_user_group == current_user_group:
        raise ValueError("Groups cannot be the same!")
    
    delete_delta = group_svc.MemberDelta(action=group_svc.MemberDelta.MemberAction.REMOVE, subject_id=user.id)
    delete_req = group_svc.UpdateGroupMembersRequest(group_id=current_user_group, member_deltas=[delete_delta])
    delete_resp = stub.UpdateMembers(delete_req)
    
    add_delta = group_svc.MemberDelta(action=group_svc.MemberDelta.MemberAction.ADD, subject_id=user.id)
    add_req = group_svc.UpdateGroupMembersRequest(group_id=new_user_group, member_deltas=[add_delta])
    add_resp = stub.UpdateMembers(add_req)

