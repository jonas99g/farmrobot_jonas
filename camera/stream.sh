ffmpeg -f v4l2 -input_format h264 -video_size 852x480 -framerate 5 -i /dev/vide>
-c:v h264 -preset veryfast -b:v 500k -maxrate 500k -bufsize 10k \
-pix_fmt yuv420p -g 10 \
-f flv "rtmp://ingest_server/streamkey" 
