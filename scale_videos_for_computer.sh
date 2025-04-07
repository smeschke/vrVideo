for f in *.MP4; do ffmpeg -i "$f" -vf "scale=1440:540" -c:v libx264 -crf 18 -r 30 -c:a copy "scaled_${f%.*}.MP4"; done
