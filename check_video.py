import cv2
import os

def get_video_info():
    video_info = []
    
    for file in os.listdir("."):  # Use current directory
        if file.lower().endswith("4"):
            cap = cv2.VideoCapture(file)
            
            if cap.isOpened():
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                video_info.append((file, width, height))
            
            cap.release()
    
    return video_info

# Run the function
videos = get_video_info()

# Print the results
for video in videos:
    print(f"File: {video[0]}, Resolution: {video[1]}x{video[2]}")

for video in videos:
    print(video[0])
