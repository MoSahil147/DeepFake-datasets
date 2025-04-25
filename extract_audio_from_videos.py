import os
import ffmpeg

# Base path
BASE_DIR = "./Datasets/faceforensics_data"
OUTPUT_DIR = "./Datasets/extracted_audio"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Dataset categories
DATASETS = {
    "manipulated_sequences": ["Deepfakes", "FaceSwap", "Face2Face"],
    "original_sequences": ["youtube"]
}

def has_audio_stream(video_path):
    """Returns True if video has audio stream, else False"""
    try:
        probe = ffmpeg.probe(video_path)
        streams = probe.get("streams", [])
        for stream in streams:
            if stream.get("codec_type") == "audio":
                return True
        return False
    except ffmpeg.Error as e:
        print(f"⚠️ Error probing: {video_path} — {e}")
        return False

# Loop over datasets
for dataset_type, subfolders in DATASETS.items():
    for sub in subfolders:
        video_dir = os.path.join(BASE_DIR, dataset_type, sub, "c23", "videos")
        output_sub_dir = os.path.join(OUTPUT_DIR, sub)
        os.makedirs(output_sub_dir, exist_ok=True)

        print(f"\n📁 Checking folder: {video_dir}")

        for file in os.listdir(video_dir):
            if file.endswith(".mp4"):
                input_path = os.path.join(video_dir, file)
                output_path = os.path.join(output_sub_dir, file.replace(".mp4", ".mp3"))

                if has_audio_stream(input_path):
                    try:
                        print(f"🎧 Extracting from: {file}")
                        (
                            ffmpeg
                            .input(input_path)
                            .output(output_path, **{'q:a': 0, 'map': 'a'})
                            .run(quiet=True, overwrite_output=True)
                        )
                        print(f"✅ Saved: {output_path}")
                    except Exception as e:
                        print(f"❌ Failed: {file} — {e}")
                else:
                    print(f"🚫 Skipped (No audio): {file}")