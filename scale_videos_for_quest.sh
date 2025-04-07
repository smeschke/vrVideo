for f in *.MP4; do ffmpeg -i "$f" -c:v libx265 -pix_fmt yuv420p -r 60 -c:a aac -b:a 128k -strict experimental "scaled_${f%.*}.MP4"; done
