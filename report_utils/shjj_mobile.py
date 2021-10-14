import requests
import json
from report_utils import des3
import datetime

headers = {
    'Host': 'sh.122.gov.cn',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Connection': 'close',
    'Accept': '*/*',
    'User-Agent': 'shang hai jiao jing/4.5.1 (iPhone; iOS 14.8; Scale/3.00)',
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
      "bbh" : "4.5.1"
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
    #url = "http://sh.122.gov.cn/shjjappapi/service/videoUp"
    #result = send_request(url, data, key, salt)
    #result_json = remove_json_pad(result)
    #print(result_json)
    #return json.loads(result_json)
    return {"code":"0","msg":"1634200926953","ydsj":"2021-10-14 16:42"}

def get_user_encypt_key(user):
    result = get_poi_ios(user)
    new_key = result["key"]
    new_salt = result["salt"]
    return new_key, new_salt

#new_key = "9c6641b379b314cfd1e66a9c"
#new_salt = "b9dc2e9d"
#info = "Vkm0j2ecMV/7K0g7GXm2cl0X4vfw/RPPEbaF3s9R1ffaGA3tZ6l1qMTRJF2p4EZB/psO21S+Eq0HzEBssH1qO1EWqmyzhwoqNNfLWFUK0vw/wnCT2rIzKorylSVvjawixBxuMsZALt2UXfpuAfPBe+ojMABNhrUMoWniKMy/4j8ISgzr6rITJAviI8SI2vu1Xl5hciIxBeI+fdxJBa2dlkJTZkRxpOC7hMY+3MHnfzSYwC3dqz2qAgu7SJ0MFV1SyPgZTy5Rx5xrWX3xj0UWwS6WgH0092wsQZrQ5C+pz9v7I6CRLNWYB0xvSOiH9E6IqfovVml6v+SiAkxz/HW7vDNGDveiq35g1HRzcjcHhA7o1ZmpOv5Mc+Bd4CnBpT/Jf0Xicce/jXHwaaXRJujVmvdtS6NJ0VdPk1py9Lyz3BxU8WtvHZuA4XufV/YFET1g4hUtKOYZ/UaIxzXNx6u1VKyNORuU37vpbTrQmeEIywnUw86fy+xOCUizj2UXK0cFrJjs+/mYr+DeAiLkcnvuQpo7SvbD5HR0Ip2Mi7PvR2KC3g8uonjJhk1URHJ7jU3mj3YZ4bjcb7Altdg8XYfIP3Ja1PGcK5wjbunxFeL2tmjGDllLdNkr7l9DBKCtcV2S7Ratw/7MpwHOuyxYO4QEPgoOh5eVKfFTrBg1UQ6vM6glUo+xF9CYQp0LapWH2Ly49BfBymgTYgTrjL3/rfSGDi2P7Dhzwp7Nu3l+twqKVvczBVSnWNfGKgmQn2GJNzhcb2xDJGotU4NB1GUwApbsBanK+rqy65xjqDzzLzQkxzBq6waDht9gFCMObxUVNq2wwGM1QD3Jl9v3JxWeulqSsX3wrG0XNa9A4+BX72CBHJ2iIyiQ/m/hpWQWyul8yRH8kNrMac721jCiLAaXmWRvnbu1DWVkUi0Zcl2NVfCBnkLx7nhLyq/O55fWvRC5unUZNFz4B/yqpHVN9TZLNUf04DOIkM78AAKPl2/aCQZIkMYDvx2rRDmVrCIunGb8CKTTnJ7ZmkCUoqhPDwhr1GXtiJcHg7IqBDMpXjNWJVLdpYESzKeeYB75b5C8nnGcYkvAYo/iNxQ1Sx7MQgiYIpZbWeXtqe4OnAiydh6eFP9PrEDe5BRMbUlqFJ6f3ZtZrLkGHd5ekHEf7MwOY/BrRi9FlSWNpY24qU+V8qCF7m/IMnB18J5TMiZexNVchaxY51VQB4rxVotiCcEp472vKfKlQoIyFjC9XunpVDqChNcjHTmTIlmrDuAAcPfEV2cqWmEsGIr7F3gzNAZEeph9c6IjDIJ/KRQbPfLl3IlePgQ1e6rZOZ6oVHu2xu5CNo/gPnrXfhGy6jwy5Ypj0loFDdAO4z/HJXiMPTnEiNZkkwyX/n4h2iMuGFPlLb3uIi0T12V0cvXR4Ijqxh1xdi/2wcKK2pfpw5WKClvz2qkXmMYDu/teFfYWEyP4YZj9iQCwgpqvFWRuTKTOjR+VSxMSmHmqelR7XKmBwNwwKulwLSJN6eSZ8q7Pz6FHOqxTY8M23Q9pLqfhF6Gl3MIuqTgolw6c6131bNyiwdIi7KUK1pWdLVojDHVfR4mGluhw5j/9ZS+HdDrxJ3Sp73gCBMvpq66wyPEdOAqhuvSnG6IZorJB+MBJvC3k7kcLgAU3vDpykwSRT/D02srgF4WK6ezNuvvJ03iN04r3bhI+kF9l4o4Ui9Mxf/hqZG39VyN9kzzzVmp6MROg2CKNEvwTXiMnVNmUoLhGKVXGroipicbl92sflpDPT6oYsa+THHGTZi+spXCKJa0R2u/FAc1nFdisqge5wltiYGMDzmSk60wT9ihlgZuMk8B1rK2JLZtF3pndsWe89ZRE/wiP7EVjmoLErxt7kybLtH8wYBkl3KkVvIdGObzFrppecrOKYQ=="
#info = "nS6AMowJX2qW2FpstIaoJEjtnHD5P+w1IC8H/EsuKQmumA2iYweG/nHRd+/V 1QQ8NUVe0NrrwCv3KPcJS1PdCUnqmJlXDyAdZL3KODgbbiE5VcOdiVOwL/yF 8m/P7s44inloRkqx+bu6/aCEUhKCpfAtJ2HT1Tua/avpW8t2kwdyjds0iwR2 CRYU2f4Ezqjxln1GXJvR2pZ5yub80aSleWMlHqbG50ZoNTrdBnDqTugyY8UO DtdsO5CqIZ731vuoj1LfDQ6mJ6cggPn+MTFEaKEwDE03Y+A5B5YAOYYLZlur yh7Gq/6oMw=="
#info = "s8uCH6gxLksAcjsO5yHPFzfK/5gl2+IiMeqtPdgjxxx7o8cJdCvgNCCVZ4de cAv5kwYkmgnI97b+S0ZxdChevE2haX7pE86kO+Jl19CbIO7w2RDVnGVKyt48 Xvds2lzxG++L0WcJJ76qFAhypCa0auyxUqCu1G9p"
#print(des3.decrypt_message(info, key=new_key, iv=new_salt))



