import logging
from storage_utils import report_info_utils

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    user_id = req.params.get("user");
    report_time = req.params.get("time");
    try:
        req_body = req.get_json()
    except ValueError:
        print("Not json body")
        pass
    else:
        report_time = req_body.get("time")
        user_id = req_body.get("user")

    if user_id is None or report_time is None:
        return func.HttpResponse("No valid user and report_time")

    report_info_utils.archive_report_info(user=user_id, report_time=report_time)
    
    return func.HttpResponse(f"ok.")
