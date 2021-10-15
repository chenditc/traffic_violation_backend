import logging
import json
import azure.functions as func

from plate.plate_recognize import *

shared_detector = None


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    video_url = req.params.get('video_url')
    if not video_url:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            video_url = req_body.get('video_url')

    if video_url is None:
        video_url = "http://1300035106.vod2.myqcloud.com/83d79a75vodcq1300035106/b325a1963701925925849484647/CambOYFKvikA.mp4"

    global shared_detector
    if shared_detector is None:
        shared_detector= PlateDetect()
    recognizer = PlateRecognize(video_url, shared_detector)
    recognizer.download()
    plates = recognizer.recognize()
    print(plates)

    # [('沪B020K9', 18.431552878447942), ('沪DX1801', 14.471312063080923), ('京DX1801', 0.8868525155952999)]
    result = [plate[0] for plate in sorted(plates, key=lambda x: -x[1])]

    return func.HttpResponse(
        json.dumps(result),
        mimetype="application/json"
        )
