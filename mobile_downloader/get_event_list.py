import get_gps_list
import requests
import json
import pathlib
import os
import tempfile

def speak_info(msg):
    try:
        import speech
        speech.say(msg)
    except:
        pass

def open_download_switch():
    download_switch_response = requests.post("http://193.168.0.1/vcam/cmd.cgi?cmd=API_SuperDownload", data='{"switch":"on"}')
    if download_switch_response.json()["errcode"] != 0:
        print(f"Failed to turn on super download: {download_switch_response.content}")

def download_url_to_path(url, path):
    download_stream = requests.get(url, stream=True)
    with open(path, 'wb') as f:
        for chunk in download_stream.iter_content(chunk_size=8192):
            f.write(chunk)

def download_all_events():
    event_list_response = requests.post("http://193.168.0.1/vcam/cmd.cgi?cmd=APP_EventListReq").json()
    if event_list_response["errcode"] == 0:
        event_list = json.loads(event_list_response["data"])["event"]
        for event in event_list:
            # Find location, if no location, skip
            #mid_time = (int(event["bstarttime"]) + int(event['bendtime'])) / 2
            gps_time = int(event["bstarttime"])
            gps_location = get_gps_list.get_gps_location_at_time(gps_time)
            print(event, gps_location)
            if gps_location is None:
                print(f"Skipping, No GPS info for event {event}")
                continue

            if "bvideoname" not in event:
                print(f"Skipping, No video info for event {event}")
                continue

            if "imgname" not in event:
                print(f"Skipping, No image info for event {event}")
                continue

            event_path = os.path.expanduser("~/Documents/traffic_violation/" + event["bvideoname"].split(".")[0])
            
            pathlib.Path(event_path).mkdir(parents=True, exist_ok=True)

            # Start download switch
            open_download_switch()

            speak_info("Start downloading video")
            # Download image
            if "imgname" in event:
                image_download_url = "http://193.168.0.1/" + event["imgname"]
                temp_image_path = event_path + "/pic1.jpg"
                download_url_to_path(image_download_url, temp_image_path)

            # Download video
            temp_video_path = event_path + "/video.mp4"
            download_video_url = "http://193.168.0.1/" + event["bvideoname"]
            print(f"Temp video path: {temp_video_path}")
            download_url_to_path(download_video_url, temp_video_path)

            # Save meta data
            meta_info = {
                "time" : gps_time,
                "lat": gps_location["lat"],
                "lon": gps_location["lon"],
            }
            meta_info_path = event_path + "/info.json"
            with open(meta_info_path, "w") as f:
                f.write(json.dumps(meta_info))

            # TODO: Delete event


