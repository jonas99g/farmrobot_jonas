ffmpeg -f v4l2 -input_format h264 -video_size 640x360 -framerate 5 -i /dev/video0 \
-c:v libx264 -preset veryfast -b:v 500k -maxrate 500k -bufsize 2000k \
-vf "format=yuv420p" -g 10 \
-f flv rtmp://fra02.contribute.live-video.net/app/[streamkey]


ffmpeg -f v4l2 -input_format h264 -video_size 1920x1080 -framerate 30 -i /dev/video0 \
-c:v libx264 -preset veryfast -b:v 4000k -maxrate 4000k -bufsize 5000k \
-vf "format=yuv420p" -g 60 \
-f flv rtmp://fra02.contribute.live-video.net/app/[streamkey]
