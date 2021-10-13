import logging
import json
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    result = [
        {
            "time":1633985212,
            "lat":31.133145,
            "lon":121.41439,
            "video_info":{
                "video":{
                    "url":"http://1300035106.vod2.myqcloud.com/83d79a75vodcq1300035106/b325aabd3701925925849484897/Syev6dNTBc8A.mp4",
                    "verify_content":"SVvY/xzSigLy7oqVGAWaNqaVSvRFeHBUaW1lPTE2MzQxMjAyNDYmRmlsZUlkPTM3MDE5MjU5MjU4NDk0ODQ4OTc="
                },
                "cover":{
                    "url":"http://1300035106.vod2.myqcloud.com/83d79a75vodcq1300035106/b325aabd3701925925849484897/3701925925849484898.jpg",
                    "verify_content":"DpKdNdg8DtjETrBhFFcOr7rsAcJFeHBUaW1lPTE2MzQxMjAyNDYmRmlsZUlkPTM3MDE5MjU5MjU4NDk0ODQ4OTg="
                },
                "fileId":"3701925925849484897"
            },
            "loc_desp":"虹梅南路 上海市徐汇区启新小学 西",
            "time_str":"2021-10-12 04:46:52",
            "plate_num":"沪D12345",
            "plate_color":0
        }
    ]
    return func.HttpResponse(
        json.dumps(result),
        mimetype="application/json"
        )

