import logging
import json
import azure.functions as func
from storage_utils import report_info_utils
from report_utils import shjj_utils

def get_plate_color(plate_num):
        # 蓝色牌照 - 0
        # 黄色牌照 - 1
        # 黄绿牌照 - 13
        # 绿色牌照 - 14
        # 其他牌照 - 2
        if len(plate_num) == 8:
                return "14"
        elif len(plate_num) == 7:
                return "0"
        return "2"

def main(req: func.HttpRequest) -> func.HttpResponse:
    user_id = req.params.get("user");
    report_json = req.params.get("report_json");
    msg_code = req.params.get("msg_code");
    try:
        req_body = req.get_json()
    except ValueError:
        print("Not json body")
        pass
    else:
        report_json = req_body.get("report_json")
        user_id = req_body.get("user")
        msg_code = req_body.get("msg_code");


    if user_id is None or report_json is None:
        return func.HttpResponse("No valid user and report_json")

    try:
        report_info = json.loads(report_json)
    except ValueError:
        return func.HttpResponse("Failed to parse report_json")

    # Add additional information
    report_info["violation_type"] = report_info.get("violation_type", "变道、转弯、掉头、靠边、起步时不打灯（不按规定使用转向灯）")
    report_info["plate_num"] = report_info.get("plate_num", "沪ADZ8655")
    report_info["plate_color"] = get_plate_color(report_info["plate_num"])

    report_info_utils.save_report_info(report_info)

    # Apply msg code if available
    user_request_info = report_info_utils.get_user_request_info(user_id)
    if user_request_info is None:
        msg = "No valid session, sending a msg code"
        user_request_info = shjj_utils.send_msg_and_get_cookie(user=user_id)
        report_info_utils.save_user_request(user_request_info=user_request_info)
        print(msg)
        return func.HttpResponse(msg)

    user_personal_info = shjj_utils.get_name_and_id_from_request_info(user_request_info=user_request_info)
    if user_personal_info is None and msg_code is not None:
        shjj_utils.apply_msg_code(user_request_info=user_request_info, msg_code=msg_code)
        user_personal_info = shjj_utils.get_name_and_id_from_request_info(user_request_info=user_request_info)

    # Trigger report
    if user_personal_info is None:
        msg = "msg code expired, resending msg code"
        user_request_info = shjj_utils.send_msg_and_get_cookie(user=user_id)
        report_info_utils.save_user_request(user_request_info=user_request_info)
        print(msg)
        return func.HttpResponse(msg)

    shjj_utils.report_violation(report_info=report_info, 
                user_personal_info=user_personal_info,
                user_request_info=user_request_info)

    return func.HttpResponse(f"ok.")
