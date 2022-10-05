from googleapiclient.discovery import build
from credentials import yt_api
import json
import time
from spotifyExtraction import query_builder

def make_publicService(yt_api):
    service = build(serviceName = 'youtube', version = 'v3', developerKey=yt_api)
    
    return service


def getVideoId(queries, api):
    service = make_publicService(api)
    ids = []
    for i in range(len(queries)):
        request = service.search().list(part="snippet", maxResults=2, q = queries[i])
        response = request.execute()
        videoid = response['items'][0]['id']['videoId']
        print(videoid)
        
        ids.append(videoid)
        time.sleep(3)
    return ids

