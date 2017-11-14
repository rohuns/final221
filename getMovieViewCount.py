# Google Developer Console API Key needed to call Youtube Data API from a web server: 
# AIzaSyCcBAJop74bcKTnXWrPid0CMJ7Szic5w-k

# # import Applications

# # python2.7.path.append('/Anaconda/lib/python2.7/site-packages')

# import os

# import google.oauth2.credentials

from googleapiclient.discovery import build #pip install google-api-python-client
from googleapiclient.errors import HttpError #pip install google-api-python-client
from oauth2client.tools import argparser #pip install oauth2client
import pandas as pd #pip install pandas


def getMovieViewCount(movieTitle):
	DEVELOPER_KEY = "AIzaSyCcBAJop74bcKTnXWrPid0CMJ7Szic5w-k" 
	YOUTUBE_API_SERVICE_NAME = "youtube"
	YOUTUBE_API_VERSION = "v3"
	argparser.add_argument("--q", help="Search term", default="%s Official Movie Trailer" % (movieTitle))
	#change the default to the search term you want to search
	argparser.add_argument("--max-results", help="Max results", default=1)
	#default number of results which are returned. It can vary from 0 - 100
	args = argparser.parse_args()
	options = args



	youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
	# Call the search.list method to retrieve results matching the specified
	 # query term.
	search_response = youtube.search().list(
	 q=options.q,
	 type="video",
	 part="id,snippet",
	 maxResults=options.max_results
	).execute()
	videos = {}
	# Add each result to the appropriate list, and then display the lists of
	 # matching videos.
	 # Filter out channels, and playlists.
	for search_result in search_response.get("items", []):
	 if search_result["id"]["kind"] == "youtube#video":
	 	#videos.append("%s" % (search_result["id"]["videoId"]))
	 	videos[search_result["id"]["videoId"]] = search_result["snippet"]["title"]
	#print "Videos:\n", "\n".join(videos), "\n"
	s = ','.join(videos.keys())

	# print videos

	# SORT BY VIEW COUNT

	videos_list_response = youtube.videos().list(
	 id=s,
	 part='id,statistics'
	).execute()
	res = []
	for i in videos_list_response['items']:
	 temp_res = dict(v_id = i['id'], v_title = videos[i['id']])
	 temp_res.update(i['statistics'])
	 res.append(temp_res)
	 
	viewCount = temp_res['viewCount']

	# print 'TEMP RES: '
	# print temp_res
	# print viewCount
	return viewCount


movieTitle = 'Inception'
count = getMovieViewCount(movieTitle)
print count
