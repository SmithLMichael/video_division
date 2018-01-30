"""
File: video_division.py
Author: Michael L. Smith

Sources:
	1. 'fireant' @ https://stackoverflow.com/questions/33311153/python-extracting-and-saving-video-frames 

Function: 
Takes all of the videos and divides them into: 
		(a) one jpeg per frame
		(b) half-second clips
		(c) 10-second clips
		(d) three parts

Dependencies: OpenCV (cv2), ffmpeg

TODO: ADD in something that works with custom file/folder names; number of clips

"""
import imageio
import sys
import argparse
import cv2
from moviepy.editor import *
import math
import ffmpeg
import os

def split_into_frames(filename, output_folder):
	vidcap = cv2.VideoCapture(filename)
	successful, image = vidcap.read()
	count = 0
	successful = True

	while successful:
		cv2.imwrite(output_folder + '/frame_%s.jpg' % count, image)
		successful, image = vidcap.read()
		count += 1

def make_video_clips(filename, output, clip_duration):
	split = False
	if clip_duration == -1:
		split = True

	video = VideoFileClip(filename)
	video_duration = video.duration

	if clip_duration == -1:
		clip_duration = video_duration / 3 # see if we can make this a variable instead..? and do some error testing on it..

	num_clips = math.floor(float(video_duration)/clip_duration) # design choice 

	# other options include: progress_bar = False, verbose = False - add these in...
	for i in range(int(num_clips)):
		clip = video.subclip(i * clip_duration, (i + 1) * clip_duration)
		if split:
			clip.write_videofile(output + '/part%d.mp4' % (i + 1), temp_audiofile="temp-audio.m4a", \
			remove_temp=True, codec="libx264", audio_codec="aac", threads=8, preset='veryfast')
		else:
			clip.write_videofile(output + '/%s-sec_clip%d.mp4' % (str(clip_duration) ,i), temp_audiofile="temp-audio.m4a", \
			remove_temp=True, codec="libx264", audio_codec="aac", threads=8, preset='veryfast')


def main(arguments):
	filename_sans_extension = os.path.basename(arguments.filename).split('.')[0]
	directory = os.path.dirname(arguments.filename)

	if directory != "":
		folder = directory + '/' + filename_sans_extension
	else:
		folder = filename_sans_extension

	if arguments.frames:
		frames_folder = folder + '_frames'
		if not os.path.exists(frames_folder):
			os.makedirs(frames_folder) # this makes a folder in the same directory as the original file
		split_into_frames(arguments.filename, frames_folder)

	if arguments.half_sec:
		half_sec_folder = folder + '_half-sec'
		if not os.path.exists(half_sec_folder):
			os.makedirs(half_sec_folder)
		make_video_clips(arguments.filename, half_sec_folder, 0.5)

	if arguments.ten_sec:
		ten_sec_folder = folder + '_ten-sec'
		if not os.path.exists(ten_sec_folder):
			os.makedirs(ten_sec_folder)
		make_video_clips(arguments.filename, ten_sec_folder, 10.0)

	if arguments.three_parts:
		three_parts_folder = folder + '_three-parts'
		if not os.path.exists(three_parts_folder):
			os.makedirs(three_parts_folder)
		make_video_clips(arguments.filename, three_parts_folder, -1)


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='This program provides the functionality to split videos.')
	parser.add_argument('--frames', help='Splits video into frames.', action='store_true')
	parser.add_argument('--all_but_frames', help='Does everything except extract frames', action='store_true')
	parser.add_argument('--half_sec', help='Splits video into half-second clips', action='store_true')
	parser.add_argument('--ten_sec', help='Splits video into ten-second clips', action='store_true')
	parser.add_argument('--three_parts', help='Splits video into three parts', action='store_true')
	parser.add_argument('filename', help='The movie path')

	arguments = parser.parse_args()

	# If no command line arguments besides program name and filename passed
	if len(sys.argv) <= 2:
		arguments.frames, arguments.half_sec, arguments.ten_sec, arguments.three_parts = (True,)*4

	if arguments.all_but_frames:
		arguments.half_sec, arguments.ten_sec, arguments.three_parts = (True,)*3
		arguments.frames = False # likely not needed, but to double check

	main(arguments)



