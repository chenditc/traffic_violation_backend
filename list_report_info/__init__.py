import logging
import json
import os
import azure.functions as func
from storage_utils import report_info_utils

def main(req: func.HttpRequest) -> func.HttpResponse:
    user_id = req.params.get("user");
    if user_id is None:
        return func.HttpResponse("No user specified")

    result = report_info_utils.list_report_info(user_id)

    for report in result:
        report["report_success"] = report.get("report_success", False)
        report["plate_candidate_list"] = report.get("plate_candidate_list", [])

    return func.HttpResponse(
        json.dumps(result),
        mimetype="application/json"
        )

