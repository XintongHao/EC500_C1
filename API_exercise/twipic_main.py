import tweepy 
import csv
import sys
import urllib
import os
import json
import io
import subprocess
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFile

from google.cloud import vision
from google.cloud.vision import types
from google.auth import app_engine

#Twitter API credentials
consumer_key = "xxx"
consumer_secret = "xxx"
access_key = "xxx"
access_secret = "xxx"



def get_twipic():
    # input user's name
    screen_name = raw_input("Whose pictures do you want to enjoy? \n(Please enter a twitter user's name) \n")  
    try:
        #authorize twitter, initialize tweepy
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_key, access_secret)
        api = tweepy.API(auth)
        new_tweets = api.user_timeline(screen_name = screen_name,count=1)
    
    except tweepy.TweepError:
        print "User does not exist:( . Please try again:)"
        return 0

    #initialize a list to hold all the tweepy Tweets
    alltweets = []    
    #directory = os.path.dirname("/screen_name") 
    path = screen_name + "_pic"
    os.makedirs(path)
 
    #save most recent tweets
    alltweets.extend(new_tweets)
    try:
        #save the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1
    except:
        print "This user haven't posted any tweets :("
        return 0

    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
            print "getting tweets before %s" % (oldest)
            #all subsequent requests use the max_id param to prevent duplicates
            new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
            #save most recent tweets
            alltweets.extend(new_tweets)
            #update the id of the oldest tweet less one
            oldest = alltweets[-1].id - 1
            print "...%s tweets downloaded so far" % (len(alltweets))
    
    #initialize master list to hold our ready tweets
    outtweets = [] 
    n = 1
    for tweet in alltweets:
            #not all tweets will have media url, so lets skip them
            try:
                    print tweet.entities['media'][0]['media_url']
            except (NameError, KeyError):
                    #we dont want to have any entries without the media_url so lets do nothing
                    pass
            else:
                    #get media_url - means add it to the output
                    outtweets.append([tweet.entities['media'][0]['media_url']])
                    # save in a directory
                    fullfilename = os.path.join( path, str(n)+'.jpg')
                    urllib.urlretrieve(tweet.entities['media'][0]['media_url'], fullfilename)
                    picLabels(tweet.entities['media'][0]['media_url'],fullfilename)
                    n += 1                   
    #write the csv  
    with open('%s_tweets.csv' % screen_name, 'wb') as f:
            writer = csv.writer(f)
            #writer.writerow(["id","created_at","text","media_url"])
            writer.writerows(outtweets)

    pass
    
    return path

def pic2vid(path):
    os.chdir(path)
    # Create a video of all the pic
    os.system("ffmpeg -framerate .5 -pattern_type glob -i '*.jpg' out.mp4")
    print '\n Create a video \n'
    return

# Instantiates a client
client = vision.ImageAnnotatorClient()
dic = {}
def picLabels(uri,fullfilename):
    image = types.Image()
    image.source.image_uri = uri
    # Get labels from Googole Vision API
    response = client.label_detection(image=image)
    labels = response.label_annotations
    print('Labels:')
    # Save all the labels in the list
    LabelList = []
    for label in labels:
        LabelList.append(label.description)
    # Dictionary for labels of each picture
    dic[fullfilename] = LabelList
    print(label.description)
    
    # Draw labels to picture
    pic = Image.open(fullfilename)
    draw = ImageDraw.Draw(pic)
    font = ImageFont.truetype("sans-serif.ttf", 15)
    shift = 0
    for label in LabelList:
        draw.text((0,shift),label, font=font)
        # Shift the postion for next label
        shift=10
    pic.save(fullfilename)
    
    return
        

def main():
    pics_path = get_twipic()
    pic2vid(pics_path)
    
    
    
    
if __name__=='__main__':
    main()
    
