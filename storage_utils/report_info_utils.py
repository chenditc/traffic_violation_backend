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
        "plate_processed" : report_info["plate_processed"],
        "archived" : False
    }
    table_client = table_service_client.get_table_client(table_name=TRAFFIC_INFO_TABLE)
    table_client.upsert_entity(entity=report_entity)

def archive_report_info(user, report_time):
    report_entity = {
        'PartitionKey': str(user), 
        'RowKey': str(report_time),
        "archived": True 
    }
    table_client = table_service_client.get_table_client(table_name=TRAFFIC_INFO_TABLE)
    table_client.update_entity(entity=report_entity)

def list_report_info(user, min_time=0):
    table_client = table_service_client.get_table_client(table_name=TRAFFIC_INFO_TABLE)
    report_list = table_client.query_entities(
        query_filter="PartitionKey eq '" + user + "' and archived ne true")
    
    result = []
    for report in report_list:
        try:
            report_info = json.loads(report["report_json"])
            if "plate_json" in report:
                report_info["plate_candidate_list"] = [ plate_info[0] for plate_info in json.loads(report["plate_json"])[:5] ]
            result.append(report_info)
        except Exception as e:
            print(e)
            pass
    return result
