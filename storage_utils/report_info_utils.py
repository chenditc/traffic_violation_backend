import os
import json
from azure.cosmosdb.table.tableservice import TableService
# https://docs.microsoft.com/en-us/azure/cosmos-db/table/how-to-use-python

table_service_client = TableService(connection_string=os.getenv("TABLE_CONNECTION_STRING"))
TRAFFIC_INFO_TABLE = "TrafficReportInfo"

def save_report_info(report_info):    
    entity = {
        'PartitionKey': report_info["user_id"], 
        'RowKey': report_info["report_id"],
        "report_json": json.dumps(report_info)
    }
    table_service_client.insert_or_replace_entity(TRAFFIC_INFO_TABLE, entity)

def list_report_info(user):
    report_list = table_service_client.query_entities(
        TRAFFIC_INFO_TABLE, 
        filter="PartitionKey eq '" + user + "'")

    result = []
    for report in report_list:
        try:
            report_info = json.loads(report["report_json"])
            result.append(report_info)
        except Exception as e:
            print(e)
            # If failed to parse, just delete it
            table_service_client.delete_entity(TRAFFIC_INFO_TABLE, report["PartitionKey"], report["RowKey"])
            pass
    return result