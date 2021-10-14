import logging
import azure.functions as func
from report_utils import shjj_utils
from storage_utils import report_info_utils

def main(req: func.HttpRequest) -> func.HttpResponse:
    user_id = req.params.get("user");
    if user_id is None:
        return func.HttpResponse("No user specified")

    user_request_info = shjj_utils.send_msg_and_get_cookie(user=user_id)
    report_info_utils.save_user_request(user_request_info=user_request_info)

    return func.HttpResponse(f"ok.")
