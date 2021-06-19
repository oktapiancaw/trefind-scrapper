import requests, sys, time, os, argparse
import urllib.request
import json 

unsafe_characters = ['\n', '"']

header = ["title",
      "publishedAt",
      "channelId",
      "channelTitle"]

def prepare_feature(feature):
  for ch in unsafe_characters:
    feature = str(feature).replace(ch, "")
  return f"{feature}"

def api_request():

  # Masukan Youtube Data API nya disini
  api_key = "GoogleApiMu"

  # Jumlah data yang diinginkan
  count_data = 20

  request_url = f"https://www.googleapis.com/youtube/v3/videos?part=id,statistics,snippet&chart=mostPopular&regionCode=ID&maxResults={count_data}&key={api_key}"
  request = requests.get(request_url)
  if request.status_code == 429:
    print("Temp-Banned due to excess requests, please wait and continue later")
    sys.exit()
  return request.json()

def get_videos(items):
  data_json = []
  session = requests.Session()
  for video in items:
    if "statistics" not in video:
      continue
    snippet = video['snippet']
    features = [prepare_feature(snippet.get(feature, "")) for feature in header]
    data = {
      'channelId': features[2],
      'title': features[0],
      'channelName': features[3],
      'publishedAt' : features[1]
    }
    url = "http://127.0.0.1:8080/api/videos/"
    session.post(url, verify=False, json=data)
    print(data)
    data_json.append(data)

  return data_json

def send_data():

  video_data_page = api_request()
  items = video_data_page.get('items', [])
  
  return get_videos(items)


if __name__ == "__main__":
  send_data()