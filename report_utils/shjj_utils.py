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

def report_violation(report_info, tel='17602144419'):
    user_request_info = send_msg_and_get_cookie(tel)
    if user_request_info is None:
        return

    sn = user_request_info["sn"]

    session = requests.session()
    requests.utils.add_dict_to_cookiejar(session.cookies, user_request_info["cookies"])

    msg_code = input("Please enter msg code")
    print(f"Msg code is {msg_code}")

    data = {
      'val17': msg_code,
      'code': '1',
      'sjhm': tel
    }
    url = 'https://sh.122.gov.cn/jb/jy'
    response = session.post(url, headers=mac_headers, data=data)
    print(response.content)
    if response.status_code != 200 or "0" in response.content.decode("utf-8"):
        print(f"Failed {url} response code: {response.status_code}")
        return 

    data = {
      'sn': sn,
      'keyVal': '',
      'u': '',
      'll': '0',
      'sjh': tel,
      'yzm': msg_code
    }
    url = 'https://sh.122.gov.cn/jb/check'
    response = session.post(url, headers=mac_headers, data=data)
    print(response.content)
    if response.status_code != 200 or sn not in response.content.decode("utf-8"):
        print(f"Failed {url} response code: {response.status_code}")
        return 

    url = f"http://sh.122.gov.cn/jb/page/save.jsp?s={sn}"
    response = session.get(url, headers=mac_headers)
    if response.status_code != 200:
        print(f"Failed {url} response code: {response.status_code}")
        return 

    submit_page_content = response.content.decode("gbk")

    name_match = re.search(r'id="val3"\s+name="val3"\s+maxlength="24"\s+value="(.*)"', submit_page_content)
    name = name_match.groups()[0]

    personal_id_match = re.search(r'id="val9"\s+name="val9"\s+maxlength="18"\s+value="(.*)"', submit_page_content)
    personal_id = name_match.groups()[0]

    data = {
      'val0': report_info["time_str"],
      'val1': report_info["loc_desp"],
      'val2': report_info["violation_type"],
      'val3': name,
      'val4': report_info["tel"],
      'val6': report_info["video_info"]["fileId"],
      'val9': personal_id,
      'val12': report_info["plate_num"][0],
      'val13': report_info["plate_num"][1:],
      'val14': report_info["plate_color"],
      'val21': '\u6CAA',
      'val22': 'AD23322',
      'val23': report_info["loc_desp"]
    }
    print(data)
    #response = session.post('https://sh.122.gov.cn/jb/save', headers=mac_headers, data=data)
