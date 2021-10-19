import requests
import json
from requests.structures import CaseInsensitiveDict
import time
import os
from qcloud_cos import CosConfig, CosS3Client

def get_signature_from_122():
    headers =  {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-language": "zh-CN,zh;q=0.9",
        "sec-ch-ua": "\"Chromium\";v=\"92\", \" Not A;Brand\";v=\"99\", \"Google Chrome\";v=\"92\"",
        "sec-ch-ua-mobile": "?0",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1"
    }
    response = requests.get("https://sh.122.gov.cn/jb/S", headers=headers)
    token = response.json()["result"]
    return token

def apply_upload_video(video_type, covert_type):
    token = get_signature_from_122()
    #2. vod service apply upload
    url = "https://vod2.qcloud.com/v3/index.php?Action=ApplyUploadUGC"

    headers = CaseInsensitiveDict()
    headers["Connection"] = "keep-alive"
    headers["Pragma"] = "no-cache"
    headers["Cache-Control"] = "no-cache"
    headers["sec-ch-ua"] = '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"'
    headers["Accept"] = "application/json, text/plain, */*"
    headers["sec-ch-ua-mobile"] = "?0"
    headers["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
    headers["Content-Type"] = "application/json;charset=UTF-8"
    headers["Origin"] = "https://sh.122.gov.cn"
    headers["Sec-Fetch-Site"] = "cross-site"
    headers["Sec-Fetch-Mode"] = "cors"
    headers["Sec-Fetch-Dest"] = "empty"
    headers["Referer"] = "https://sh.122.gov.cn/"
    headers["Accept-Language"] = "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6"

    data = {
            "signature": token,
            "videoType": video_type,
            "coverType": covert_type
    }

    resp = requests.post(url, headers=headers, data=json.dumps(data))
    video_upload_info = resp.json()["data"]
    return video_upload_info

def upload_video_using_cos(video_upload_info, local_file_path):
    cos_config = CosConfig(
        Region="ap-chongqing",
        SecretId=video_upload_info["tempCertificate"]["secretId"],
        SecretKey=video_upload_info["tempCertificate"]["secretKey"],
        Token=video_upload_info["tempCertificate"]["token"]
    )
    cos_client = CosS3Client(cos_config)

    print("start upload")
    cos_client.upload_file(
                    Bucket=video_upload_info["storageBucket"] + "-" + str(video_upload_info["storageAppId"]),
                    LocalFilePath=local_file_path,
                    Key=video_upload_info["video"]["storagePath"]
                )
    print("Complete upload")

def upload_picture_using_cos(video_upload_info, local_file_path):
    cos_config = CosConfig(
        Region="ap-chongqing",
        SecretId=video_upload_info["tempCertificate"]["secretId"],
        SecretKey=video_upload_info["tempCertificate"]["secretKey"],
        Token=video_upload_info["tempCertificate"]["token"]
    )
    cos_client = CosS3Client(cos_config)

    print("start upload")
    cos_client.upload_file(
                    Bucket=video_upload_info["storageBucket"] + "-" + str(video_upload_info["storageAppId"]),
                    LocalFilePath=local_file_path,
                    Key=video_upload_info["cover"]["storagePath"]
                )
    print("Complete upload")

def commit_upload(video_upload_info):
    token = get_signature_from_122()

    # Commit upload
    url = "https://vod2.qcloud.com/v3/index.php?Action=CommitUploadUGC"

    headers = CaseInsensitiveDict()
    headers["Connection"] = "keep-alive"
    headers["Pragma"] = "no-cache"
    headers["Cache-Control"] = "no-cache"
    headers["sec-ch-ua"] = '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"'
    headers["Accept"] = "application/json, text/plain, */*"
    headers["sec-ch-ua-mobile"] = "?0"
    headers["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
    headers["Content-Type"] = "application/json;charset=UTF-8"
    headers["Origin"] = "https://sh.122.gov.cn"
    headers["Sec-Fetch-Site"] = "cross-site"
    headers["Sec-Fetch-Mode"] = "cors"
    headers["Sec-Fetch-Dest"] = "empty"
    headers["Referer"] = "https://sh.122.gov.cn/"
    headers["Accept-Language"] = "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6"

    data = {
        "vodSessionKey": video_upload_info["vodSessionKey"],
        "signature": token 
    }

    resp = requests.post(url, headers=headers, data=json.dumps(data))
    video_info = resp.json()["data"]
    return video_info

def upload_shanghai_jiaojing_video(video_file_path, cover_file_path):
    video_upload_info = apply_upload_video(video_file_path.split(".")[-1], cover_file_path.split(".")[-1])
    upload_video_using_cos(video_upload_info, video_file_path)
    upload_picture_using_cos(video_upload_info, cover_file_path)
    return commit_upload(video_upload_info)
