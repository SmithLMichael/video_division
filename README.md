# video_division

This program currently has the functionality to take in a video (for example, video.mp4 on your desktop) or its pathname, and can split it up 4 ways, with each method organized into its own folder in the same file location as the video. 

Those ways include:
1. Split entire video into its frames
2. Split video into half-second clips
3. Split video into ten-second clips
4. Split video into three parts

*(Future functionality will be to separate a video into k parts given a command line argument, as well as a custom clip duration)

Command line arguments:
1. Default: all 4 above are run
2. --frames, --all_but_frames, --half_sec, --ten_sec, --three_parts, filename

When you use --all_but_frames, you will run ways 2-4 above. When you only call --half_sec, you will only get half-sec clips back. If you call --ten_sec and --three_parts, then you will get both ten-sec clips AND your video split into three clips. And so on and so forth.

Dependencies/programs needed to run this:
1. Python 2.7
2. moviepy
3. imageio (downloaded as part of moviepy)
4. ffmpeg 
5. OpenCV (I've elected to use ver. 3.4.0, the most currrent at time of release)

Suggestions for use:
1. It might be prudent to download all those dependences into a virtual environment (like virtualenv)
2. When subdividing the videos into clips, the program calls the floor function to determine the number of clips given a specific clip duration. Hence, if you want ten second clips, and you input a 25 second video, you will get floor(25/10) = 2 clips, one from 0-10 sec, and the other from 10-20 sec. The last 5 seconds will be disregarded. This is something that can modified if needed.
