import logging
import json
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    result = [
        {
            "time":1634072173,
            "lat":31.123072,
            "lon":121.420892,
            "video_info":{
                "video":{
                    "url":"http://1300035106.vod2.myqcloud.com/83d79a75vodcq1300035106/72ba400f3701925925862524839/TtsiHAoLe6YA.mp4",
                    "verify_content":"rAkuZYtuDDM+n9vQpELMBc3uAnVFeHBUaW1lPTE2MzQxMTc3MjkmRmlsZUlkPTM3MDE5MjU5MjU4NjI1MjQ4Mzk="
                },
                "fileId":"3701925925862524839"
            },
            "loc_desp":"莘朱路 外环虹梅南路立交桥 西",
            "time_str":"2021-10-13 04:56:13",
            "plate_num":"沪D12345",
            "plate_color":0
        }
    ]
    return func.HttpResponse(
        json.dumps(result),
        mimetype="application/json"
        )

