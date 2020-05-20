import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

from oauth2client import client # Added
from oauth2client import tools # Added
from oauth2client.file import Storage # Added

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

#formatting changes
from html import unescape
import csv
import math

CLIENT_SECRETS_FILE = 'client_secret.json'

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account.
SCOPES = ['https://www.googleapis.com/auth/youtube']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

#writes individual video info
def insertQuery(feed, diff, stack):
    
    item  = feed['items']
    items = item[:diff]
    print(len(item))
    print(len(items))
    print(items)
    for video in items:
        videoid = (video['snippet']['resourceId']['videoId'])
        print(videoid + ' pushed into stack')
        stack.append(videoid)

def main():
    
    #Default retrieval and authentication from Youtube/Oauth2
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret.json"

    # Get credentials and create an API client
    # Credentials created from google developer page
    credential_path = os.path.join('./', 'credential_sample.json')
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRETS_FILE, SCOPES)
        credentials = tools.run_flow(flow, store)
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    #video initial parameters
    pageToken = None
    minrange = 1
    maxrange = 50
    page = 1
    maxResult = 50
         

    privateRequest = youtube.playlistItems().list(part="snippet",playlistId="INSERT YOUTUBE PLAYLIST",maxResults=maxResult, pageToken=pageToken)
    privateFeed = privateRequest.execute()
    privateTotal = privateFeed['pageInfo']['totalResults']

    publicRequest = youtube.playlistItems().list(part="snippet",playlistId="INSERT YOUTUBE PLAYLIST",maxResults=maxResult, pageToken=pageToken)
    publicFeed = publicRequest.execute()
    publicTotal = publicFeed['pageInfo']['totalResults']

    diff = privateTotal - publicTotal
    print(privateTotal)
    print(publicTotal)
    print("there is a difference of ", diff)
    stack = []

    if diff<=50:
        print('Getting page:', page, ' Results [', minrange, '-' , diff, ']')
        insertQuery(privateFeed, diff, stack)

    else:
        totalparts=math.ceil(diff/50)
        maxResult = 50
        for part in range(totalparts):
            print('Getting page:', page ,'| Results [', minrange, '-', maxrange, ']')
            privateRequest = youtube.playlistItems().list(part="snippet",playlistId="INSERT YOUTUBE PLAYLIST",maxResults=maxResult, pageToken=pageToken)
            privateFeed = privateRequest.execute()
            insertQuery(privateFeed, diff, stack)
            diff = diff-50
            try:
                pageToken = privateFeed['nextPageToken']
            except:
                total = privateFeed['pageInfo']['totalResults']
                print('maximum search results found: ', total)
                break
            if part==(totalparts-2) and diff%50 != 0:
                maxResult = diff%50
            minrange = minrange + 50
            maxrange = maxrange + maxResult
            page += 1

    for a in range(len(stack)):
        break
        vid = stack.pop()
        request = youtube.playlistItems().insert(
            part="snippet",
            body={
              "snippet": {
                "playlistId": "INSERT YOUTUBE PLAYLIST",
                "resourceId": {
                  "kind": "youtube#video",
                  "videoId": vid
                }
              }
            }
        )

        response = request.execute()
        print(a+1, 'video(s) added to playlist')
        
#run main function
if __name__ =="__main__":
    main()

