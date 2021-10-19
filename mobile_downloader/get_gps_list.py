import requests
import json
import load_git
from io import BytesIO

def download_gps_file_and_load_info(filename):
    tar_file_content = requests.get(f"http://193.168.0.1/{filename}", stream=True).content
    return load_git.parse_git_tar_stream(BytesIO(tar_file_content))

def find_closest_location_obj(target_time, gps_list):
    if len(gps_list) == 0:
        return
    return min(gps_list, key=lambda x: abs(x["time"].timestamp() - target_time))

def get_gps_location_at_time(target_time):
    gps_file_list_response = requests.post("http://193.168.0.1/vcam/cmd.cgi?cmd=API_GpsFileListReq").json()
    if gps_file_list_response["errcode"] == 0:
            gps_file_list = json.loads(gps_file_list_response["data"])
            for gps_file in gps_file_list['file']:
                    if target_time > int(gps_file["endtime"]):
                            continue
                    if target_time < int(gps_file["starttime"]):
                            continue
                    if gps_file["type"] != "50":
                            continue
                    gps_list = download_gps_file_and_load_info(gps_file["name"])
                    return find_closest_location_obj(target_time, gps_list)
