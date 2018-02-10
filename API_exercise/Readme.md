# Twitter API 
main file [Preview](https://github.com/XintongHao/EC500_C1/blob/master/API_exercise/twipic_main.py)

### Requirement
```
tweepy
ffmpy
google-cloud-vision
```

### Step
1. Download the ["twipic_main.py"](https://github.com/XintongHao/EC500_C1/blob/master/API_exercise/twipic_main.py) file. Fill in the Twitter API credentials.
( If your Google Vision API credential does not work, like mine, please test [twipic_twi.py](https://github.com/XintongHao/EC500_C1/blob/master/API_exercise/twipic_twi.py) 
2. Run the file and enter the Twitter user's name in the console.
3. Check the directory. You will see a csv file with all the picture's url in it, and a new directory with all the pictures and a video in it.
4. 

## Google Vision API
Python file [Preview](https://github.com/XintongHao/EC500_C1/blob/master/API_exercise/picLabels.py)
### Step
1. Build a new project in Google Cloud Platform. Enable Google Cloud Vision API and install all the libraries.
2. Create credentials for the project and get a json file and the service account.
3. Get authentation in terminal. Run gcloud to enter into the account and select the project
4. Write python: Open all the pictures which were downloaded from user's twitter --> Get client and response from Google Cloud Vision API --> Get 'Label' response from Vision API --> Append all the labels and the content of one picture into a json file.
5. Draw the label texts into picture by using PIL library.
