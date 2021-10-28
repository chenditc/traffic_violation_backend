import logging
import json
import os
import time
import azure.functions as func
from storage_utils import report_info_utils
from report_utils import enrich_report_info

def main(req: func.HttpRequest) -> func.HttpResponse:
    user_id = req.params.get("user");
    refresh_info = req.params.get("refresh_info");
    if user_id is None:
        return func.HttpResponse("No user specified")

    result = report_info_utils.list_report_info(user_id)

    if len(result) > 0:
        last_week = time.time() - 3600 * 24 * 7
        result = sorted(result, key=lambda x: x["time"], reverse=True)
        result = [x for x in result if x["time"] > last_week]
    
    for report in result:
        report["report_success"] = report.get("report_success", False)
        report["plate_candidate_list"] = report.get("plate_candidate_list", [])
        if report.get("plate_num", "") == "" and len(report["plate_candidate_list"]) > 0:
            report["plate_num"] = report["plate_candidate_list"][0]
    
    if refresh_info:
        for report in result:
            enrich_report_info.enrich_report_info(report)
            report_info_utils.save_report_info(report)

    return func.HttpResponse(
        json.dumps(result),
        mimetype="application/json"
        )

