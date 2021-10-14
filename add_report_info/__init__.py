import logging
import os
import azure.functions as func
import uuid

from azure.cosmosdb.table.tableservice import TableService
# https://docs.microsoft.com/en-us/azure/cosmos-db/table/how-to-use-python

def main(req: func.HttpRequest) -> func.HttpResponse:
    user_id = req.params.get("user");
    report_json = req.params.get("report_json");
    try:
        req_body = req.get_json()
    except ValueError:
        pass
    else:
        report_json = req_body.get('report_json')
        user_id = req_body.get('user_id')

    if user_id is None or report_json is None:
        return func.HttpResponse(f"Failed to pase body")

    report_id = str(uuid.uuid4())

    conn_str = os.getenv("TABLE_CONNECTION_STRING")
    table_service = TableService(connection_string=conn_str)
    entity = {
        'PartitionKey': user_id, 
        'RowKey': report_id,
        "report_json": report_json
    }
    table_service.insert_entity('TrafficReportInfo', entity)

    return func.HttpResponse(f"ok")
