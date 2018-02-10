import json
import io
import os
from google.cloud import vision
from google.cloud.vision import types
from google.auth import app_engine
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFile

# Instantiates a client
client = vision.ImageAnnotatorClient()
dic = {}
def picLabels(uri,fullfilename):
    image = types.Image()
    image.source.image_uri = uri
    response = client.label_detection(image=image)
    labels = response.label_annotations
    print('Labels:')
    
    LabelList = []
    for label in labels:
        LabelList.append(label.description)
        
    dic[fullfilename] = LabelList
    print(label.description)
    
    # Draw label to picture
    pic = Image.open(fullfilename)
    draw = ImageDraw.Draw(pic)
    font = ImageFont.truetype("sans-serif.ttf", 15)
    shift = 0
    for label in LabelList:
        draw.text((0,shift),label, font=font)
        shift=10
    pic.save(fullfilename)
    
    return
        