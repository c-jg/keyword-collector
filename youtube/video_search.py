import os

import googleapiclient.discovery
import googleapiclient.errors


class SearchQuery:
	def __init__(self, keyword, query):
		self.keyword = keyword 
		self.query = query
		self.youtube = self.build_yt() 
		self.results = {
			"Title": [],
			"URL": []
		}

	def build_yt(self):
		# Disable OAuthlib's HTTPS verification when running locally.
		# *DO NOT* leave this option enabled in production.
		os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

		scopes = ["https://www.googleapis.com/auth/youtube"]

		api_service_name = "youtube"
		api_version = "v3"
		API_KEY = os.environ["YT_API_KEY"]
		
		youtube = googleapiclient.discovery.build(
			api_service_name, api_version, developerKey=API_KEY)

		return youtube

	def search(self, page_token=None):
		request = self.youtube.search().list(
			part="snippet",
			q=self.query,
			maxResults=50,
			safeSearch="none",
			type="video",
			pageToken=page_token
		)
		response = request.execute()

		videos = response["items"]
		for video in videos:
			self.results["Title"].append(video['snippet']["title"])

			url = video['id']['videoId']
			self.results["URL"].append(url)

		retrieved = len(self.results["URL"])
		if "nextPageToken" in response and retrieved < 200:
			return self.search(page_token=response["nextPageToken"])

		search_results = self.results["URL"]

		return search_results
