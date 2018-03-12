import twitter
import json
import urllib.request
import urllib

import os
import subprocess
from google.cloud import videointelligence
from google.oauth2 import service_account
from google.protobuf.json_format import MessageToJson

class InvalidMediaException(Exception):
    pass

class InvalidCredentialsException(Exception):
	pass

def get_timeline_media_urls(screen_name, count=200, exclude_replies=True): 
	"""Get list of jpg urls found in media associated with tweets from a specific twitter accounts timeline

    Args:
        screen_name (str): Twitter screen name associated with desired timeline

    Keyword Arguments (optional):
        count (int): Number of tweets to look through (capped at 200 per api limits). Default 200.
        exclude_replies (bool): Exclude media found in tweets where specified user only replied. Default: True

    Returns:
        list: All .jpg image urls found in the twitter feed, as strings. 

    """
	with open("keys.dat") as f:
		keys = f.read().split()
	try:
		api = twitter.Api(consumer_key= keys[0],
					consumer_secret=keys[1],
					access_token_key=keys[2],
					access_token_secret=keys[3])
	except:
		raise InvalidCredentialsException("Invalid twitter credentials")

	try:
		res = api.GetUserTimeline(screen_name=screen_name, count=count, trim_user=True, exclude_replies=exclude_replies)
	except Exception as e:
		raise e
	images = []
	for tweet in res:
		js = tweet._json["entities"]
		if "media" in js.keys():
			for media in js["media"]:
				if media["media_url"][-3:] == "jpg":
					images.append(media["media_url"])
					
	if len(images) == 0:
		raise InvalidMediaException("No valid media found for screen_name: " + screen_name)

	with open("test_img.txt", "w") as f:
		for i in range(len(images)):
			f.write("file 'tmp_{}.jpg'\n".format(str(i).zfill(4)))
	
	path = screen_name + "_pic"
	os.makedirs(path)

	for i in range(len(images)):
		try:
			fullfilename = os.path.join( path, "tmp_{}.jpg".format(str(i).zfill(4)))
			urllib.request.urlretrieve(images[i], filename= fullfilename)
		except Exception as e:
			raise e


	return images


if __name__ == "__main__":
	get_timeline_media_urls("dffsdfdfsdf", count=10, exclude_replies=True)