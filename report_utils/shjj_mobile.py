import requests
import json
from report_utils import des3
import datetime
import os

SHJJ_VERSION="4.6.5"

headers = {
    'Host': 'sh.122.gov.cn',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Connection': 'close',
    'Accept': '*/*',
    'User-Agent': 'shang hai jiao jing/' + SHJJ_VERSION + ' (iPhone; iOS 14.8; Scale/3.00)',
    'Accept-Language': 'zh-Hans-CN;q=1, en-CN;q=0.9, zh-Hant-CN;q=0.8, ko-CN;q=0.7',
    'Content-Length': '472',
    'Accept-Encoding': 'gzip, deflate',
}

def send_request(url, data, key=None, salt=None):
	  data_str = des3.encrypt_message(json.dumps(data), key, salt)
	  response = requests.post(url, headers=headers, data=data_str, verify=False)
	  if response.status_code != 200:
		    print(f"request failed: {response.content}")
		    return
	  return des3.decrypt_message(response.content, key, salt)

def remove_json_pad(input_str):
    return "}".join(input_str.split("}")[:-1]) + "}"

def get_curr_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_poi_ios(user):
    curr_time = get_curr_time()
    data = {
      "systemname" : "iOS",
      "phonename" : "",
      "identifiernumber" : "19F27B44-E042-4E9F-BBBA-65BE09381FD8",
      "qqsj" : curr_time,
      "totalmemorysize" : "3960438784",
      "phoneNum" : user,
      "mac" : "020000000000",
      "devicelanguage" : "zh-Hans-CN",
      "phoneType" : "iPhone",
      "version" : "14.8",
    }
    url = 'http://sh.122.gov.cn/shjjappapi/service/getPoiIos'

    result = send_request(url, data)
    result_json = remove_json_pad(result)
    print(result_json)
    return json.loads(result_json)

def login(user, password, key, salt):
    data = {
      "username" : user,
      "password" : password,
      "phoneType" : "ios",
      "qqsj" : get_curr_time(),
      "bbh" : SHJJ_VERSION
    }
    url = "http://sh.122.gov.cn/shjjappapi/service/login"
    result = send_request(url, data, key, salt)
    result_json = remove_json_pad(result)
    print(result_json)
    return json.loads(result_json)

def report_video(report_info, user_login_info, key, salt):

    data = {
      "xzqh" : report_info["loc_response"]["XZQH"],
      "username" : report_info["tel"],
      "spdz" : report_info["video_info"]["fileId"],
      "qqsj" : get_curr_time(),
      "hpys" : report_info["plate_color"],
      "hphm" : report_info["plate_num"],
      "sfzhm" : user_login_info["sfzh"],
      "cjsb" : "4",
      "userToken" : user_login_info["userToken"],
      "id" : "",
      "roadlist" : json.dumps(report_info["loc_response"]),
      "wfsj" : report_info["time_str"],
      "yhid" : report_info["tel"],
      "wfdd" : report_info["loc_response"]["GaoDeMiaoShu"],
      "zjh" : user_login_info["sfzh"],
      "xm" : user_login_info["xm"],
      "wfxw" : report_info["violation_type"],
      "bz" : "",
      "sjhm" : report_info["tel"],
      "gps" : "{},{}".format(report_info["gcj_lng"], report_info["gcj_lat"])
    }
    print(data)
    if os.environ.get("REAL_REPORT"):
      url = "http://sh.122.gov.cn/shjjappapi/service/videoUp"
      result = send_request(url, data, key, salt)
      result_json = remove_json_pad(result)
      print(result_json)
      return json.loads(result_json)
    else:
      return {"code":"0","msg":"1634200926953","ydsj":"2021-10-14 16:42"}

def get_user_encypt_key(user):
    result = get_poi_ios(user)
    new_key = result["key"]
    new_salt = result["salt"]
    return new_key, new_salt




