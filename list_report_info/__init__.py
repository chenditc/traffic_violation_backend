import logging
import json
import os
import azure.functions as func
from storage_utils import report_info_utils
from report_utils import enrich_report_info

def main(req: func.HttpRequest) -> func.HttpResponse:
    user_id = req.params.get("user");
    refresh_info = req.params.get("refresh_info");
    if user_id is None:
        return func.HttpResponse("No user specified")

    result = report_info_utils.list_report_info(user_id)

    for report in result:
        report["report_success"] = report.get("report_success", False)
        report["plate_candidate_list"] = report.get("plate_candidate_list", [])
    
    if refresh_info:
        for report in result:
            enrich_report_info.enrich_report_info(report)
            report_info_utils.save_report_info(report)

    return func.HttpResponse(
        json.dumps(result),
        mimetype="application/json"
        )

