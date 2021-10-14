import os.path
import pathlib
import re
from collections import defaultdict
from urllib import request

import cv2
from hyperlpr import HyperLPR_plate_recognition
from strsimpy.jaro_winkler import JaroWinkler

from plate_detect import PlateDetect


class PlateRecognize:

    def __init__(self, video_url, detector):
        self.detector = detector
        self.video_url = video_url
        work_folder = pathlib.Path().resolve()
        video_name = video_url.split('/')[-1]
        self.video_folder = os.path.join(work_folder, "../video")
        self.video_file = os.path.join(self.video_folder, video_name)
        self.image_folder = os.path.join(work_folder, "../image", video_name.split('.')[0])
        self.re = re.compile(
            "([京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼使领]{1}[A-Z]{1}(([A-HJ-NP-Z0-9]{5}[DF]{1})|([DF]{1}[A-HJ-NP-Z0-9]{5})))|([京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼使领]{1}[A-Z]{1}[A-HJ-NP-Z0-9]{4}[A-HJ-NP-Z0-9挂学警港澳]{1})")
        self.jarowinkler = JaroWinkler()

    def download(self):
        pathlib.Path(self.video_folder).mkdir(parents=True, exist_ok=True)
        request.urlretrieve(url, self.video_file)

    def recognize(self):
        pathlib.Path(self.image_folder).mkdir(parents=True, exist_ok=True)
        video_capture = cv2.VideoCapture(self.video_file)
        fps = int(video_capture.get(cv2.CAP_PROP_FPS))
        success, image = video_capture.read()
        count = 0
        plate_dict = defaultdict(lambda: 0)
        while success:
            if (count + 1) % (fps * 1) == 0:
                x, y, _ = image.shape
                image = image[0:int(x * 0.8), 0:y]
                for i, loc in enumerate(detector.detect(count, image)):
                    x0, y0, x1, y1 = (round(x) for x in loc)
                    xl, yl = abs(x1 - x0), abs(y1 - y0)
                    img_raw = image[max(0, y0 - yl):y1 + yl, max(0, x0 - xl):x1 + xl]
                    height, width, *_ = img_raw.shape
                    if not height or not width:
                        continue
                    for plate, score, *_ in HyperLPR_plate_recognition(img_raw):
                        # print(f"PLATE {count}-{i}", plate, score)
                        if score > 0.85 and self.re.findall(plate):
                            plate_dict[plate] += score
            success, image = video_capture.read()
            count += 1

        group = {x: {x} for x in plate_dict.keys()}
        for k0 in plate_dict.keys():
            score = [(self.jarowinkler.similarity(k0, k1), k1) for k1 in plate_dict.keys() if k0 != k1]
            first = sorted(score, reverse=True)[0]
            if first[0] > 0.95:
                group[k0] = group[k0].union(group[first[1]])
                group[first[1]] = group[k0]

        result = {}
        merged = set()
        for key in plate_dict.keys():
            if key not in merged:
                merged = merged.union(group[key])
            max_key = max((plate_dict[k], k) for k in group[key])
            result[max_key[1]] = sum(plate_dict[k] for k in group[key])

        return sorted(result.items(), key=lambda x: x[1], reverse=True)


if __name__ == '__main__':
    # url = "http://1300035106.vod2.myqcloud.com/83d79a75vodcq1300035106/20f956b53701925925895653755/J1i9LoTbjVsA.mp4"
    url = "http://1300035106.vod2.myqcloud.com/83d79a75vodcq1300035106/b325a1963701925925849484647/CambOYFKvikA.mp4"

    detector = PlateDetect()
    recognizer = PlateRecognize(url, detector)
    recognizer.download()
    plates = recognizer.recognize()
    print(plates)
