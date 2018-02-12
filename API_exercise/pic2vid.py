def pic2vid(path):
    os.chdir(path)
    # Create a video of all the pic
    os.system("ffmpeg -framerate .5 -pattern_type glob -i '*.jpg' out.mp4")
    print 'Create a video \n'
    return
