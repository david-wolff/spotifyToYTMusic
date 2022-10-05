import json
import os
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle

from google_auth_oauthlib.flow import InstalledAppFlow

from youtubeSearch import make_publicService

def makeService():
    credentials = None
    
    if os.path.exists("token.pickle"):
        print("Loading Credentials From File")
        with open("token.pickle", "rb") as token:
            credentials = pickle.load(token)
    
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            print("Refreshing Access Token...")
            credentials.refresh(Request())
        else:
            print("Fetching new tokens")
            flow = InstalledAppFlow.from_client_secrets_file("client_secrets.json", scopes=["https://www.googleapis.com/auth/youtube"])
            
            flow.run_local_server(
                port=8080, prompt="consent", authorization_prompt_message=""
            )
            credentials = flow.credentials

            # Save the credentials for the next run
            with open("token.pickle", "wb") as f:
                print("Saving Credentials for Future Use...")
                pickle.dump(credentials, f)

    service = build(serviceName="youtube", version="v3", credentials=credentials)

    return service

def makePlaylist(serv, name):
    request = serv.playlists().insert(
        part="snippet", body={"snippet": {"title":str(name)}}
    )
    
    response = request.execute()
    return response['id']

def addItemToPlaylist(service, pl_id, items):
    res = []
    for i in items:
        request = service.playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                    "playlistId": str(pl_id),
                    "resourceId": {"kind": "youtube#video", "videoId": i},
                }
            },
        )
        response = request.execute()
        print("Added")
        res.append(response)

    return res            