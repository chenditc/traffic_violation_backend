from upload_video import upload_shanghai_jiaojing_video
from get_event_list import download_all_events
from enrich_report_info import enrich_report_info
import os
import json
import datetime
import requests
import time

DEFAULT_DIRECTORY = os.path.expanduser("~/Documents/traffic_violation/")

def upload_video_and_generate_report_form(target_directory=DEFAULT_DIRECTORY):
	report_form = {}
	# Check local directories that needs report
	for root, directories, files in os.walk(target_directory):
		print(root)
		if len(files) == 0:
			continue

		if "report_form.json" in files:
			print(f"already processed for {root}")
			continue

		# Run plate check from image
		if "pic1.jpg" not in files:
			continue
		image_file_path = os.path.join(root, "pic1.jpg")

		# Convert time and location info
		if "info.json" not in files:
			continue
		with open(os.path.join(root, "info.json")) as json_file:
			report_form = json.load(json_file)
		
		# Upload video
		if "video.mp4" not in files:
			continue

		video_file_path = os.path.join(root, "video.mp4")
		#video_info = {'video': {'url': 'http://1300035106.vod2.myqcloud.com/83d79a75vodcq1300035106/20f956b53701925925895653755/J1i9LoTbjVsA.mp4', 'verify_content': 'uwt/9kwheJAU24EcZoOF6P6aULxFeHBUaW1lPTE2MzQwMjQxODcmRmlsZUlkPTM3MDE5MjU5MjU4OTU2NTM3NTU='}, 'fileId': '3701925925895653755'}
		video_info = upload_shanghai_jiaojing_video(video_file_path, image_file_path)
		report_form["video_info"] = video_info
		enrich_report_info(report_form)

		# Save form info to local storage
		with open(os.path.join(root, "report_form.json"), "w") as report_form_file:
			json.dump(report_form, report_form_file)
			print(report_form)

		# Submit report form to cloud
		url = "https://traffic-violation.azurewebsites.net/api/add_report_info"
		data = {"user": "17602144419", "report_json" : json.dumps(report_form)}
		requests.post(url, data=json.dumps(data))

if __name__ == "__main__":
	download_all_events()
	upload_video_and_generate_report_form()
