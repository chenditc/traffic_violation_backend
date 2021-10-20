import re
import requests
import time
import datetime
from dateutil import tz
from report_utils.coord_convert import wgs84_to_gcj02

mac_headers = {
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://sh.122.gov.cn',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://sh.122.gov.cn/jb/',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6',
}

def get_report_type_from_video(video_file_path):
 #    摩托车闯禁令
 #    大型车辆污损、遮挡号牌
 #    机动车噪声污染
 #    驾车时浏览电子设备
 #    摩托车占用公交车道
 #    机动车未按规定交替通行
 #    货车未按规定黏贴反光标志
 #    闯禁令（违反禁令标志指示）
 #    驾驶摩托车时未佩戴安全头盔
 #    路间黄实线处左转或调头（违反禁止标线指示）
 #    实线变道（违反禁止标线指示）
 #    逆向行驶（机动车逆向行驶的）
 #    车窗抛物（向道路上抛洒物品）
 #    压斑马线（违反禁止标线指示）
 #    货车上高架（违反禁令标志指示）
 #    黄实线停车（违反禁止标线指示）
 #    机动车载物行驶时遗撒、飘散载运物
 #    机动车载货长度、宽度、高度超过规定
 #    占用应急车道（占用应急车道行驶的）
 #    不按导向车道行驶（不按导向车道行驶）
 #    变道、转弯、掉头、靠边、起步时不打灯（不按规定使用转向灯）
 #    转弯不让直行（转弯车不让直行车或行人）
 #    占用公交车道（机动车违规使用专用车道）
 #    货车占客车道（机动车违规使用专用车道）
 #    路口滞留（交通拥堵处不按规定停车等候）
 #    开车打电话（驾车时拨打接听手持电话的）
 #    不避让特种车辆（不避让执行任务特种车辆）
 #    不在机动车道内行驶（机动车不走机动车道）
 #    危险路段掉头（在容易发生危险的路段掉头的）
 #    闯红灯（驾驶机动车违反道路交通信号灯通行的）
 #    未避让行人（遇行人正在通过人行横道时未停车让行的）
 #    连续变换两条车道（驾驶机动车一次连续变换两条车道）
 #    违反规定掉头（在禁止掉头或者禁止左转弯标志、标线的地点掉头的）
 #    红灯时超越停车线（通过路口遇停止信号时，停在停止线以内或路口内的）
 #    加塞（遇前方机动车停车排队时，借道超车或者占用对面车道、穿插等候车辆的）
 #    拥堵时在人行横道、网格线内停车（遇前方机动车停车排队等候或者缓慢行驶时，在人行横道、网状线区域内停车等候的）
        return "加塞（遇前方机动车停车排队时，借道超车或者占用对面车道、穿插等候车辆的）"

def convert_time_str(epoch_time):
    utc_time = datetime.datetime.utcfromtimestamp(epoch_time)
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('Asia/Shanghai')
    local_time = utc_time.replace(tzinfo=from_zone).astimezone(to_zone)
    return local_time.strftime("%Y-%m-%d %H:%M:%S")

def convert_time_no_timezone(epoch_time):
    return datetime.datetime.utcfromtimestamp(epoch_time).strftime("%Y-%m-%d %H:%M:%S")

def get_report_location_from_lat_lon(lat, lon):
    new_lng, new_lat = wgs84_to_gcj02(lon, lat)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
    }
    url = f"http://sh.122.gov.cn/position/Service/GetLocation.ashx?x={new_lng}&y={new_lat}&date={time.time()}"
    print(url)
    max_retry = 5
    for i in range(max_retry):
        try:
            loc_response = requests.get(url, headers=headers)
            loc_response = loc_response.json()
        except Exception as e:
            print("Failed to get gps info")
            if i == (max_retry - 1):
                throw e
    return loc_response

def enrich_report_info(report_info):
    report_info["gcj_lng"], report_info["gcj_lat"] = wgs84_to_gcj02(report_info["lon"], report_info["lat"])
    report_info["loc_response"] = get_report_location_from_lat_lon(report_info["gcj_lat"], report_info["gcj_lng"])
    report_info["time_str"] = convert_time_no_timezone(report_info["time"])
    return report_info
