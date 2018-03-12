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
			# 	cwd=os.path.dirname(os.path.realpath(__file__)), shell=True, env=dict(os.environ, PATH="ffmpeg-20180201-b1af0e2-win64-static/bin"))
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
			
	#cleanup temp files
	for i in range(len(images)):
		os.remove("tmp_{}.jpg".format(str(i).zfill(4)))
		os.remove("tmp_{}.mp4".format(str(i).zfill(4)))
	# os.remove("tmp_files.txt".format(str(i).zfill(4)))

	return output

def video_analysis(filename):
	"""Generate list of labels for a specified mp4 file, using Google cloud ideo intelligence

	Ouput is of form: 
		[{start: 0, end: 1, labels: [("cat", .56), ("animal>dog", .2)]}]
		Each labels is broken up by (category > categy > ... > entity , confidence level)

    Args:
        filename (str): Filename of input .mp4 file

    Returns:
        list: list of segments and labels, sorted by start time of each shot

    """
	credentials = service_account.Credentials.from_service_account_file(
	    'googe.dat')
	try:
		client = videointelligence.VideoIntelligenceServiceClient(
			credentials=credentials
		)
	except Exception as e:
		raise e

	try:
		with open(filename, "rb") as f:
			video_data = f.read()
	except Exception as e:
		raise e

	try:
		result = client.annotate_video(
			input_content=video_data,
			features=['LABEL_DETECTION'],
		).result()
	except Exception as e:
		raise e

	return result

def get_twitter_media_analysis(screen_name, count=200, exclude_replies=True, output_name="output.mp4", delete_movie=True):
	"""Generate list of labels from the video anaylsis of a specified users twitter timeline

	Ouput is of form: 
		[{start: 0, end: 1, labels: [("cat", .56), ("animal>dog", .2)]}]
		Each labels is broken up by (category > categy > ... > entity , confidence level)

    Args:
       screen_name (str): Twitter screenname associated with desired timeline

    Keyword Arguments (optional):
       count (int): Number of tweets to look through (capped at 200 per api limits). Default: 200
       exclude_replies (bool): Exclude media found in tweets where specified user only replied. Default: True
       output_name (str): Filename of input .mp4 file. Default: output.mp4
	   delete_movie (bool): Specified whether or not to remove local file after analysis. Default: True

    Returns:
        list: list of segments and labels, sorted by start time of each shot

    """
	images = get_timeline_media_urls(screen_name, count, exclude_replies)
	output_filename_actual = urls_to_movie(images, output=output_name)
	result = video_analysis(output_filename_actual)
	if delete_movie:
		os.remove(output_name)

	analysis_json = json.loads(MessageToJson(result)) 

	segments = dict()
	#only one video submitted
	for shot_label in analysis_json["annotationResults"][0]["shotLabelAnnotations"]:
		entity = [shot_label["entity"]["description"]]
		if "categoryEntities" in shot_label.keys():
			for category_entity in shot_label["categoryEntities"]:
				entity.append(category_entity["description"])
			entity = entity[::-1]

		entity = ">".join(entity)

		for segment in shot_label["segments"]:
			seg = segment["segment"]
			time = (float(seg["startTimeOffset"][:-1]), float(seg["endTimeOffset"][:-1]))
			if time not in segments.keys():
				segments[time] = dict(start=time[0], end=time[1], labels=[(entity, segment["confidence"])])
			else:
				segments[time]["labels"].append((entity, segment["confidence"]))

	results = []
	for key in segments.keys():
		results.append(segments[key])
	results = sorted(results, key= lambda x: x["start"])
	
	return results

if __name__ == "__main__":
	get_twitter_media_analysis("dannygarcia95", count=10)
