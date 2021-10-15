import logging
import json
import azure.functions as func
import report_utils
import os
from storage_utils import report_info_utils
from report_utils import shjj_utils
from report_utils import enrich_report_info
from report_utils import shjj_mobile

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
    try:
        req_body = req.get_json()
    except ValueError:
        print("Not json body")
        pass
    else:
        report_json = req_body.get("report_json")
        user_id = req_body.get("user")

    if user_id is None or report_json is None:
        return func.HttpResponse("No valid user and report_json")

    try:
        report_info = json.loads(report_json)
    except ValueError:
        return func.HttpResponse("Failed to parse report_json")

    logging.info("Enriching additional report info")
    enrich_report_info.enrich_report_info(report_info)
    report_info["violation_type"] = report_info.get("violation_type", "")
    report_info["plate_num"] = report_info.get("plate_num", "")
    report_info["plate_color"] = get_plate_color(report_info["plate_num"])

    logging.info("Saving report info")
    logging.info(report_info)
    report_info_utils.save_report_info(report_info)

    logging.info("Logging into shjj")
    password = os.environ.get("SHJJ_PASSWORD")
    user_key, user_salt = shjj_mobile.get_user_encypt_key(user_id)
    user_login_info = shjj_mobile.login(user_id, password, user_key, user_salt)
    print(user_login_info)

    logging.info("Submitting report")
    report_result = shjj_mobile.report_video(report_info, user_login_info=user_login_info, key=user_key, salt=user_salt)

    if report_result["code"] == "0":
        report_info["report_success"] = True
        report_info["report_success_reason"] = report_info.get("report_success_reason", [])
        report_info["report_success_reason"].append(report_info["violation_type"])

    logging.info("Saving report")
    report_info_utils.save_report_info(report_info)

    return func.HttpResponse(f"ok.")
