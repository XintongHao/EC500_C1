import twitter
import json
import urllib.request
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
	return images

def urls_to_movie(images, output="output.mp4"):
	"""Generate local mp4 file from a list of urls, with 1 sec per images

    Args:
        images (list): List of images to include in movie, as strings

	Keyword Arguments (optional):
        output: Ouput filename for video. Default: output.mp4

    Returns:
        str: Output filename used by ffmpeg, in event provided filename was in use

    """
	count = 0
	while os.path.isfile(output):
		output = output.split(".")[0] + "(" + str(count) + ")." + output.split(".")[1]
		count += 1

	for i in range(len(images)):
		try:
			urllib.request.urlretrieve(images[i], "tmp_{}.jpg".format(str(i).zfill(4)))
		except Exception as e:
			raise e

	for i in range(len(images)):
		try:
			os.system(('''ffmpeg -loop 1 -i tmp_{}.jpg -c:a libfdk_aac -ar 44100 -ac 2 -vf "scale='if(gt(a,16/9),1280,-1)':'if(gt(a,16/9),-1,720)', pad=1280:720:(ow-iw)/2:(oh-ih)/2" -c:v libx264 -b:v 10M -pix_fmt yuv420p -r 30 -shortest -avoid_negative_ts make_zero -fflags +genpts -t 1 tmp_{}.mp4''').format(str(i).zfill(4) , str(i).zfill(4)))
			# subprocess.call(('''ffmpeg -loop 1 -i tmp_{}.jpg -c:a libfdk_aac -ar 44100 -ac 2 -vf "scale='if(gt(a,16/9),1280,-1)':'if(gt(a,16/9),-1,720)',                                  pad=1280:720:(ow-iw)/2:(oh-ih)/2" -c:v libx264 -b:v 10M -pix_fmt yuv420p -r 30 -shortest -avoid_negative_ts make_zero -fflags +genpts -t 1 tmp_{}.mp4''').format(str(i).zfill(4) , str(i).zfill(4)),
			# 	cwd=os.path.dirname(os.path.realpath(__file__)), shell=True, env=dict(os.environ, PATH="/Users/yt.hao/Desktop/BU/Study/EC500C1/CodeReview/EC500-master/Test_Xintong/Test2_urls_to_movie/ffmpeg-3.4.2"))
		except Exception as e:
			raise e

	with open("tmp_files.txt", "w") as f:
		for i in range(len(images)):
			f.write("file 'tmp_{}.mp4'\n".format(str(i).zfill(4)))

	try:
		subprocess.call("ffmpeg -f concat -i tmp_files.txt " + output,
			cwd=os.path.dirname(os.path.realpath(__file__)),
			shell=True,
			env=dict(os.environ))
	except Exception as e:
		raise e
			
			
	# cleanup temp files
	for i in range(len(images)):
		os.remove("tmp_{}.jpg".format(str(i).zfill(4)))
		os.remove("tmp_{}.mp4".format(str(i).zfill(4)))
	# os.remove("tmp_files.txt".format(str(i).zfill(4)))

	return output



if __name__ == "__main__":
	images = get_timeline_media_urls("charlieputh", count=200, exclude_replies=True)
	urls_to_movie(images, output="output.mp4")

