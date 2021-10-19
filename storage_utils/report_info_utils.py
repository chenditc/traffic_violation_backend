import os
import json
from azure.data.tables import TableServiceClient
# https://docs.microsoft.com/en-us/azure/cosmos-db/table/how-to-use-python

connection_string=os.getenv("TABLE_CONNECTION_STRING");
table_service_client = TableServiceClient.from_connection_string(conn_str=connection_string)
TRAFFIC_INFO_TABLE = "TrafficReportInfo"
USER_REQUEST_TABLE = "UserRequestInfo"


def save_report_info(report_info):    
    report_info["plate_processed"] = report_info.get("plate_processed", False)
    
    report_entity = {
        'PartitionKey': str(report_info["user_id"]), 
        'RowKey': report_info["report_id"],
        "report_json": json.dumps(report_info),
        "plate_processed" : report_info["plate_processed"]
    }
    table_client = table_service_client.get_table_client(table_name=TRAFFIC_INFO_TABLE)
    table_client.upsert_entity(entity=report_entity)

def list_report_info(user):
    table_client = table_service_client.get_table_client(table_name=TRAFFIC_INFO_TABLE)
    report_list = table_client.query_entities(
        query_filter="PartitionKey eq '" + user + "'")

    result = []
    for report in report_list:
        try:
            report_info = json.loads(report["report_json"])
            if "plate_json" in report:
                report_info["plate_candidate_list"] = [ plate_info[0] for plate_info in json.loads(report["plate_json"])[:5] ]
            result.append(report_info)
        except Exception as e:
            print(e)
            # If failed to parse, just delete it
            # table_client.delete_entity(TRAFFIC_INFO_TABLE, report["PartitionKey"], report["RowKey"])
            pass
    return result

def save_user_request(user_request_info):
    user = str(user_request_info["user"])
    request_entity = {
        'PartitionKey': user, 
        'RowKey': user,
        "request_info": json.dumps(user_request_info)
    }
    table_client = table_service_client.get_table_client(table_name=USER_REQUEST_TABLE)
    table_client.upsert_entity(entity=request_entity)

def get_user_request_info(user):
    table_client = table_service_client.get_table_client(table_name=USER_REQUEST_TABLE)
    result_list = list(table_client.query_entities(
        query_filter="PartitionKey eq '" + user + "'"))

    if len(result_list) == 0:
        return

    request_info = json.loads(result_list[0]["request_info"])
    return request_info
