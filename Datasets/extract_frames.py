import cv2
import os
from glob import glob

def extract_frames(video_path, output_dir, frame_size=(128, 128), every_n=10):
    print(f"Processing: {video_path}")  # NEW: Show current video being processed
    os.makedirs(output_dir, exist_ok=True)
    cap = cv2.VideoCapture(video_path)
    frame_num = 0
    saved_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_num % every_n == 0:
            frame = cv2.resize(frame, frame_size)
            filename = f"{output_dir}/frame_{frame_num:04d}.jpg"
            cv2.imwrite(filename, frame)
            saved_count += 1

        frame_num += 1

    cap.release()
    print(f"Saved {saved_count} frames to {output_dir}\n")  # NEW: Output saved frame count
    return saved_count

# Example usage
video_files = glob('faceforensics_data/**/*.mp4', recursive=True)
print(f"Total videos found: {len(video_files)}")  # NEW: Confirm how many videos are detected

for video in video_files:
    class_label = 'real' if 'original_sequences' in video else 'fake'
    video_name = os.path.splitext(os.path.basename(video))[0]
    out_path = f"frames/{class_label}/{video_name}"
    extract_frames(video, out_path) . 