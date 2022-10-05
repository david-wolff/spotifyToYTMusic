from credentials import my_client_secret, my_client_id,yt_api
from spotifyExtraction import connect,fetch_playlist_by_id,extract_data,query_builder, pl_id
from youtubeOAuth import makePlaylist, addItemToPlaylist, makeService
from youtubeSearch import getVideoId





def main(pl_id):
    
    api = connect(my_client_id,my_client_secret)
    items_name = fetch_playlist_by_id(api,pl_id)
    name = items_name[1]
    queries = query_builder(extract_data(api,items_name[0]))
    videoIds = getVideoId(queries,yt_api)
   
    service = makeService()
    new_play_id = makePlaylist(service,name)
    addItemToPlaylist(service,new_play_id,videoIds)
    print("finished migrating")
    # return queries
    return new_play_id



print(main(pl_id))