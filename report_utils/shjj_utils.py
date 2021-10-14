import re
import requests

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

def get_session_from_request_info(user_request_info):
    session = requests.session()
    session.headers.update(mac_headers)
    requests.utils.add_dict_to_cookiejar(session.cookies, user_request_info["cookies"])
    return session

def send_msg_and_get_cookie(user):
    session = requests.session()
    # Get sn number
    response = session.get("http://sh.122.gov.cn/jb/page/default.jsp", headers=mac_headers)
    sn_match = re.search(r'<input type="hidden" value="(.*)" id="sn" name="sn"', response.content.decode("UTF-8"))
    if not sn_match:
        print("Failed to find sn match")
        return

    sn = sn_match.groups()[0]
    print(f"sn is: {sn}")

    # send msg and get validate info
    data = {
      'sjhm': user,
      'code': '1'
    }
    response = session.post('https://sh.122.gov.cn/jb/sendMsg', headers=mac_headers, data=data)

    user_request_info = {
        "sn": sn,
        "user": user,
        "cookies": requests.utils.dict_from_cookiejar(session.cookies)
    }
    if len(user_request_info["cookies"]) == 0:
        print("Failed to get user cookies")
        return
    print(f"User request info {user_request_info}")
    return user_request_info

def get_name_and_id_from_request_info(user_request_info):
    sn = user_request_info["sn"]
    session = get_session_from_request_info(user_request_info=user_request_info)
    url = f"http://sh.122.gov.cn/jb/page/save.jsp?s={sn}"
    response = session.get(url)
    if response.status_code != 200:
        print(f"Failed {url} response code: {response.status_code}")
        return 

    try:
        submit_page_content = response.content.decode("gbk")
    except:
        print("Failed to parse response")
        return

    name_match = re.search(r'id="val3"\s+name="val3"\s+maxlength="24"\s+value="(.*)"', submit_page_content)
    if name_match is None:
        return
    name = name_match.groups()[0]

    personal_id_match = re.search(r'id="val9"\s+name="val9"\s+maxlength="18"\s+value="(.*)"', submit_page_content)
    if personal_id_match is None:
        return
    personal_id = personal_id_match.groups()[0]

    return { "name" : name, "personal_id": personal_id }

def apply_msg_code(user_request_info, msg_code):
    session = get_session_from_request_info(user_request_info=user_request_info)

    data = {
      'val17': msg_code,
      'code': '1',
      'sjhm': user_request_info["user"]
    }
    url = 'https://sh.122.gov.cn/jb/jy'
    response = session.post(url, headers=mac_headers, data=data)
    print(response.content)
    if response.status_code != 200 or "0" in response.content.decode("utf-8"):
        print(f"Failed {url} response code: {response.status_code}")
        return 

    data = {
      'sn': user_request_info["sn"],
      'keyVal': '',
      'u': '',
      'll': '0',
      'sjh': user_request_info["user"],
      'yzm': msg_code
    }
    url = 'https://sh.122.gov.cn/jb/check'
    response = session.post(url, headers=mac_headers, data=data)
    print(response.content)
    if response.status_code != 200 or user_request_info["sn"] not in response.content.decode("utf-8"):
        print(f"Failed {url} response code: {response.status_code}")
        return 

def report_violation(report_info, user_personal_info, user_request_info):
    data = {
      'val0': report_info["time_str"],
      'val1': "浦东-中环高架内侧虹梅高架上匝道",
      'val2': report_info["violation_type"],
      'val3': user_personal_info["name"],
      'val4': report_info["tel"],
      'val6': report_info["video_info"]["fileId"],
      'val9': user_personal_info["personal_id"],
      'val12': report_info["plate_num"][0],
      'val13': report_info["plate_num"][1:],
      'val14': report_info["plate_color"],
      'val21': '\u6CAA',
      'val22': 'AD23322',
      'val23': "",
    }
    print(data)
    sn = user_request_info["sn"]
    other_headers = {
        "Referer": f"https://sh.122.gov.cn/jb/page/save.jsp?s={sn}"
    }
    session = get_session_from_request_info(user_request_info=user_request_info)
    response = session.post('https://sh.122.gov.cn/jb/save', headers=other_headers, data=data)
    print(response.status_code)
    print(response.content)