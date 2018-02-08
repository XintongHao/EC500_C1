import tweepy 
import csv
import sys
import urllib
import os

#Twitter API credentials
consumer_key = "gwMkbWfPcZE9TAXekRDEpwNIm"
consumer_secret = "e07vq6fsJSbbFRpgOboh0B3yokdUGnzpu2bXjE7nVcdZM26wGP"
access_key = "2683176107-HNvFrkYZgYlGFzsP0BTUejTQxONTuIODD5jliAt"
access_secret = "QJ05rOrGVvOIB5vLaHST1UbVbuu5OpIznI8KOPKXuBAgL"



def get_twipic():
    # input user's name
    screen_name = raw_input("Whose pictures do you want to enjoy? \n(Please enter a twitter user's name) \n")
    
    #authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)    

    #initialize a list to hold all the tweepy Tweets
    alltweets = []
       
    #directory = os.path.dirname("/screen_name") 
    path = screen_name + "_pic"
    os.makedirs(path)
 
    #make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name = screen_name,count=1)  
    
    #save most recent tweets
    alltweets.extend(new_tweets)
    
    #save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

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


    #go through all found tweets and remove the ones with no images 
    
    #initialize master list to hold our ready tweets
    outtweets = [] 
    
    for tweet in alltweets:
            #not all tweets will have media url, so lets skip them
            try:
                    print tweet.entities['media'][0]['media_url']
            except (NameError, KeyError):
                    #we dont want to have any entries without the media_url so lets do nothing
                    pass
            else:
                    #got media_url - means add it to the output
                    #outtweets.append([tweet.id_str, tweet.created_at, tweet.text.encode("utf-8"), tweet.entities['media'][0]['media_url']])
                    outtweets.append([tweet.entities['media'][0]['media_url']])
                    fullfilename = os.path.join( path, tweet.id_str+'.jpg')
                    urllib.urlretrieve(tweet.entities['media'][0]['media_url'], fullfilename)

    #write the csv  
    with open('%s_tweets.csv' % screen_name, 'wb') as f:
            writer = csv.writer(f)
            #writer.writerow(["id","created_at","text","media_url"])
            writer.writerows(outtweets)

    pass
    
    return path

def pic2vid(path):
    os.chdir(path)
    # Rename all the pic
    os.system('j=1; for i in *.jpg; do mv "$i" "$j".jpg; let j=j+1;done')
    # Create a video of all the pic
    os.system("ffmpeg -framerate .5 -pattern_type glob -i '*.jpg' out.mp4")
    print 'Create a video \n'
    return


    

def main():
    pics_path = get_twipic()
    pic2vid(pics_path)
    
    
    
if __name__=='__main__':
    main()
    