# EC500

### Dependencies

All of the package dependecies are available via pip. This module is built in Python 3.

Required python libraries:
* python-twitter: https://github.com/bear/python-twitter
* Google Cloud Video Intelligence: https://cloud.google.com/video-intelligence/docs/reference/libraries#client-libraries-install-python

Extenal dependencies:
* ffmpeg: Location of ffmpeg executable must exist in user PATH environment variable.

### API Keys

Two API Keys are required, one for Twitter and one for Google Video Intelligence.

Twitter keys should be put in a file named keys.dat in the local directory, with all 4 keys spearated by new lines.

For Video Intelligence, the service account file created via the Google Cloud Console should be placed in a file named googe.dat in the working directory. 

### Usage 
The overall functionality is exposed via:
~~~~
get_twitter_media_analysis(screen_name, count=200, exclude_replies=True, output_name='output.mp4', delete_movie=True)
~~~~

The individual functions are broken out into their own API's. 
All errors are pass through, meaning that all of these calls should be surrounded in a try-catch architecture. 

### Example

~~~~
import twitter_to_movie
print(twitter_to_movie.get_twitter_media_analysis("dannygarcia95", count=10))
~~~~

### Help Module Contents

~~~~
NAME
    twitter_to_movie

FUNCTIONS
    get_timeline_media_urls(screen_name, count=200, exclude_replies=True)
        Get list of jpg urls found in media associated with tweets from a specific twitter accounts timeline
        
        Args:
            screen_name (str): Twitter screen name associated with desired timeline
        
        Keyword Arguments (optional):
            count (int): Number of tweets to look through (capped at 200 per api limits). Default 200.
            exclude_replies (bool): Exclude media found in tweets where specified user only replied. Default: True
        
        Returns:
            list: All .jpg image urls found in the twitter feed, as strings.
    
    get_twitter_media_analysis(screen_name, count=200, exclude_replies=True, output_name='output.mp4', delete_movie=True)
        Generate list of labels from the video anaylsis of a specified users twitter timeline
        
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
    
    urls_to_movie(images, output='output.mp4')
        Generate local mp4 file from a list of urls, with 1 sec per images
        
        Args:
            images (list): List of images to include in movie, as strings
        
            Keyword Arguments (optional):
            output: Ouput filename for video. Default: output.mp4
        
        Returns:
            str: Output filename used by ffmpeg, in event provided filename was in use
    
    video_analysis(filename)
        Generate list of labels for a specified mp4 file, using Google cloud ideo intelligence
        
            Ouput is of form: 
                    [{start: 0, end: 1, labels: [("cat", .56), ("animal>dog", .2)]}]
                    Each labels is broken up by (category > categy > ... > entity , confidence level)
        
        Args:
            filename (str): Filename of input .mp4 file
        
        Returns:
            list: list of segments and labels, sorted by start time of each shot
~~~~

### Author

John Delaney
