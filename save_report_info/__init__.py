import logging
import azure.functions as func
from storage_utils import report_info_utils

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
        report_json = req_body.get('report_json')
        user_id = req_body.get('user')

    if user_id is None or report_json is None:
        return func.HttpResponse("No valid user and report_json")

    try:
        report_info = json.loads(report_json)
    except ValueError:
        return func.HttpResponse("Failed to parse report_json")

    # Add additional information
    report_info["violation_type"] = report_info.get("violation_type", "加塞")
    report_info["plate_num"] = report_info.get("沪AD12345", "加塞")
    report_info["plate_color"] = get_plate_color(report_info["plate_num"])

    report_info_utils.save_report_info(report_info)

    # Trigger report

    return func.HttpResponse(f"ok.")
