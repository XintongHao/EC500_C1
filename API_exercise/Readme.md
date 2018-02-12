# Twitter API 
main file [Preview](https://github.com/XintongHao/EC500_C1/blob/master/API_exercise/twipic_main.py)

### Requirement
```
tweepy
ffmpy
google-cloud-vision
PIL
( font "sans-serif.ttf" )
```

### Step
1. Download the ["twipic_main.py"](https://github.com/XintongHao/EC500_C1/blob/master/API_exercise/twipic_main.py) file. 
Remember to fill in the Twitter API credentials.
( If your Google Vision API credential does not work, like mine, please test [twipic_twi.py](https://github.com/XintongHao/EC500_C1/blob/master/API_exercise/twipic_twi.py) 
2. Run the file and enter the Twitter user's name in the console.
3. Check the directory. You will see a csv file with all the picture's url in it, and a new directory with all the pictures and a video in it.


## Google Vision API
Python file [Preview](https://github.com/XintongHao/EC500_C1/blob/master/API_exercise/picLabels.py)
( This file with some unknown reason, doesn't work in my Macbook Air. But this file has tested in other's PC and worked. )
### To make it work, you have to 
1. Have a Google Cloud Platform. Enable Google Cloud Vision API and install all google-cloud libraries.
2. Create credentials for the project and get a json file and the service account.
3. Get authentation in terminal. Run gcloud to enter into the account and select the project


### Error Condtitions
1. Twitter user's screen name doesn't exist & This user doesn't have any tweets: return 0 and show error content.
2. FFmepg doesn't work: No content of " Create a video"
3. Google Vision API doesn't response: I have this problems in my own PC, and I have not solved it yet. It seems that the only way to solve this error is to use another computer to test... :( .......
