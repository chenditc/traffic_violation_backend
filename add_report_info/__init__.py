import logging
import os
import json
import azure.functions as func
import uuid
from storage_utils import report_info_utils

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
    report_id = str(report_info["time"])
    report_info["report_id"] = report_id
    report_info["tel"] = user_id
    report_info["user_id"] = user_id

    report_info_utils.save_report_info(report_info)

    return func.HttpResponse(f"ok")
