import logging
import json
import os
import azure.functions as func

from azure.cosmosdb.table.tableservice import TableService


def main(req: func.HttpRequest) -> func.HttpResponse:
    user_id = req.params.get("user");
    if user_id is None:
        return func.HttpResponse("No user specified")
    conn_str = os.getenv("TABLE_CONNECTION_STRING")
    table_service = TableService(connection_string=conn_str)
    report_list = table_service.query_entities(
        'TrafficReportInfo', 
        filter="PartitionKey eq '" + user_id + "'")

    result = []
    for report in report_list:
        try:
            report_info = json.loads(report["report_json"])
            result.append(report_info)
        except Exception as e:
            print(e)
            # If failed to parse, just delete it
            table_service.delete_entity('TrafficReportInfo', report["PartitionKey"], report["RowKey"])
            pass

    return func.HttpResponse(
        json.dumps(result),
        mimetype="application/json"
        )

