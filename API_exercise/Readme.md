# Twitter API 
Python file [Preview](https://github.com/XintongHao/EC500_C1/blob/master/API_exercise/tweet_image_dumper.py)
### Step
1. Learn from Tweepy Library. 
2. Find the module which meets our requirement: Authorization module, Timeline module, Entities module (eg. entities['media']）
3. Access to a point user's twitter and download all the picture in [pic directory](https://github.com/XintongHao/EC500_C1/tree/master/API_exercise/pic1) Example User : charlieputh
4. Store all the url of all the pictures in a [csv file](https://github.com/XintongHao/EC500_C1/blob/master/API_exercise/charlieputh_tweets.csv).
5. Use ffmpeg get video per image in the pic directory. [commandline] (https://github.com/XintongHao/EC500_C1/blob/master/API_exercise/commandline.txt)
6. concatenate all the videos together [view](https://github.com/XintongHao/EC500_C1/blob/master/API_exercise/MP4/output.mp4)

## Google Vision API
Python file [Preview](https://github.com/XintongHao/EC500_C1/blob/master/API_exercise/ImageFeature.py)
### Step
1. Build a new project in Google Cloud Platform. Enable Google Cloud Vision API and install all the libraries.
2. Create credentials for the project and get a json file and the service account.
3. Get authentation in terminal. Run gcloud to enter into the account and select the project
4. Write python: Open all the pictures which were downloaded from user's twitter --> Get client and response from Google Cloud Vision API --> Get 'Label' response from Vision API --> Append all the labels and the content of one picture into a json file.
