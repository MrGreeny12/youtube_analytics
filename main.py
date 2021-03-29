# -*- coding: utf-8 -*-
import json
import os
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/yt-analytics.readonly']

API_SERVICE_NAME = 'youtubeAnalytics'
API_VERSION = 'v2'
CLIENT_SECRETS_FILE = 'client_secret_218835884873-0725ferkojb2t5g1hht3fsd9l5i7e6sn.apps.googleusercontent.com.json'


def get_service():
  flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
  credentials = flow.run_console()
  return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)


def execute_api_request(client_library_function, **kwargs):
  response = client_library_function(
    **kwargs
  ).execute()

  return response


class Data:

  def __init__(self, jsonFile, youtubeData):
    self.file = jsonFile
    self.data = youtubeData


  def createJson(self):
    '''
    take youtube-data
    :return: data.json
    '''
    with open('data.json', 'w') as f:
      json.dump(self.data, f)
      print('Done')


  def reformateJsonFile(self):
    '''
    takes the json - file and changes the need txt - format
    :return: data.txt
    '''
    self.createJson()
    with open(self.file, 'r') as f:
      data = json.loads(f.read())
      count = 0
      for i in data['rows']:
          if count == 0:
            entry = 'Date, Views' + '\n'
            count += 1
            with open('data.txt', 'w') as file:
              file.write(entry)
          else:
            date = i[0]
            views = str(i[1])
            viewsCount = date + ',' + views + '\n'
            with open('data.txt', 'a') as file:
              file.write(viewsCount)
    print('Done')


if __name__ == '__main__':
  os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

  youtubeAnalytics = get_service()
  youtubeData = execute_api_request(
    youtubeAnalytics.reports().query,
    ids='channel==MINE',
    startDate='2019-04-10',
    endDate='2021-03-25',
    metrics='views',
    dimensions='day',
    sort='day',
    prettyPrint=True,
    filters='video==X4fb6gaqITA',
  )
  myVideo = Data(jsonFile='data.json', youtubeData=youtubeData)
  myVideo.reformateJsonFile()