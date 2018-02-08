def pic2vid(path):
    os.chdir(path)
    # Rename all the pic
    os.system('j=1; for i in *.jpg; do mv "$i" "$j".jpg; let j=j+1;done')
    # Create a video of all the pic
    os.system("ffmpeg -framerate .5 -pattern_type glob -i '*.jpg' out.mp4")
    print 'Create a video \n'
    return