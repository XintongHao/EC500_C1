from ffmpy import FFmpeg
import os

path = '/pic'

for filename in os.listdir(path):
	ff = ffmpy.FFmpeg(
		inputs = { filename : None }
		outputs = { filename+'.mp4' : '-c:a libfdk_aac -ar 44100 -ac 2 -vf "scale='if(gt(a,16/9),1280,-1)':'if(gt(a,16/9),-1,720)', pad=1280:720:(ow-iw)/2:(oh-ih)/2" -c:v libx264 -b:v 10M -pix_fmt yuv420p -r 30 -shortest -avoid_negative_ts make_zero -fflags +genpts -t 1'}
		)
ff.cmd
ff.run()

# ffmpeg -loop 1 -i [INPUT FILENAME] -c:a libfdk_aac -ar 44100 -ac 2 -vf "scale='if(gt(a,16/9),1280,-1)':'if(gt(a,16/9),-1,720)', pad=1280:720:(ow-iw)/2:(oh-ih)/2" -c:v libx264 -b:v 10M -pix_fmt yuv420p -r 30 -shortest -avoid_negative_ts make_zero -fflags +genpts -t 1 OUTPUTFILENAME.mp4