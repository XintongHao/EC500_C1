import argparse
import base64
import json
import sys
import io
import os

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

# Instantiates a client
client = vision.ImageAnnotatorClient()


def main(input_file, output_filename):
    """Translates the input file into a json output file.

    Args:
        input_file: a file object, containing lines of input to convert.
        e.g. april_hao.cvs, a file contains all the twitter pictures of user april_hao
        output_filename: the name of the file to output the json to
    """
    request_list = []
    for line in input_file:
        image_filename

        with open(image_filename, 'rb') as image_file:
            content_json_obj = {
                'content': base64.b64encode(image_file.read()).decode('UTF-8')
            }

        image = types.Image(content=content)

        # Performs label detection on the image file
        response = client.label_detection(image=image)
        labels = response.label_annotations
        labels_pic = []
        for label in labels:
            labels_pic.append(label.description)


        request_list.append({
            'labels': labels_pic,
            'image': content_json_obj,
        })


    with open(output_filename, 'w') as output_file:
        json.dump({'requests': request_list}, output_file)


