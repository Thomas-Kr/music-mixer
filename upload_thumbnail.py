#!/usr/bin/python
import os

from apiclient.discovery import build
from apiclient.errors import HttpError

from upload_video import get_authenticated_service


# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret. You can acquire an OAuth 2.0 client ID and client secret from
# the {{ Google Cloud Console }} at
# {{ https://cloud.google.com/console }}.
# Please ensure that you have enabled the YouTube Data API for your project.
# For more information about using OAuth2 to access the YouTube Data API, see:
#   https://developers.google.com/youtube/v3/guides/authentication
# For more information about the client_secrets.json file format, see:
#   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
CLIENT_SECRETS_FILE = "client_secrets.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account.
YOUTUBE_READ_WRITE_SCOPE = "https://www.googleapis.com/auth/youtube"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# This variable defines a message to display if the CLIENT_SECRETS_FILE is
# missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:

	 %s

with information from the {{ Cloud Console }}
{{ https://cloud.google.com/console }}

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
																	 CLIENT_SECRETS_FILE))

# Call the API's thumbnails.set method to upload the thumbnail image and
# associate it with the appropriate video.
def upload_thumbnail(youtube, video_id, file):
	youtube.thumbnails().set(
		videoId=video_id,
		media_body=file
	).execute()

def upload_YT_thumbnail(youtube, videoID, file):
	try:
		upload_thumbnail(youtube, videoID, file)
	except HttpError as e:
		print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
	else:
		print("The custom thumbnail was successfully set.")