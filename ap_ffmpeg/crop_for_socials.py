import anchorpoint as ap
import apsync as aps
import subprocess
import os
import ffmpeg_helper
import subprocess

ui = ap.UI()
ctx = ap.get_context()
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = ctx.path


# Define the directory where the files are located
directory = file_path

###-----------------------------------------------------------------------------------------

def convert_video_to_social(input_file):
    ffmpeg_path = ffmpeg_helper.get_ffmpeg_fullpath()
    ffprobe_path = r"C:/Program Files/ffmpeg/bin/ffprobe.exe" #needs to be global


    if not os.path.exists(input_file):
        print("Input file does not exist.")
        return

    filename, extension = os.path.splitext(ctx.path)

    output_directory = f"{filename}_SOCIAL"
    os.makedirs(output_directory, exist_ok=True)

    output_file_16x9 = os.path.join(output_directory, f"{filename}_16x9{extension}")
    output_file_9x16 = os.path.join(output_directory, f"{filename}_9x16{extension}")

    ffprobe_cmd = [ffprobe_path, "-v", "error", "-select_streams", "v:0", "-show_entries",
                   "stream=width,height", "-of", "csv=p=0", input_file]

    ffprobe_output = subprocess.check_output(ffprobe_cmd).decode().strip().split(',')
    input_width = int(ffprobe_output[0])
    input_height = int(ffprobe_output[1])

    output_width_16x9 = input_width
    output_height_16x9 = output_width_16x9 * 9 // 16

    output_width_9x16 = input_height * 9 // 16
    output_height_9x16 = input_height

    max_resolution = max(input_width, input_height)

    if output_width_16x9 > max_resolution:
        output_width_16x9 = max_resolution
    if output_height_16x9 > max_resolution:
        output_height_16x9 = max_resolution
    if output_width_9x16 > max_resolution:
        output_width_9x16 = max_resolution
    if output_height_9x16 > max_resolution:
        output_height_9x16 = max_resolution

    ffmpeg_cmd_16x9 = [
        ffmpeg_path, "-i", input_file, "-vf",
        f"crop=w=iw:h=trunc(iw*9/16),scale={output_width_16x9}:{output_height_16x9}",
        "-c:v", "libx264", "-crf", "23", "-c:a", "copy", output_file_16x9
    ]

    ffmpeg_cmd_9x16 = [
        ffmpeg_path, "-i", input_file, "-vf",
        f"crop=w=trunc(ih*9/16):h=ih,scale={output_width_9x16}:{output_height_9x16}",
        "-c:v", "libx264", "-crf", "23", "-c:a", "copy", output_file_9x16
    ]

    subprocess.call(ffmpeg_cmd_16x9)
    subprocess.call(ffmpeg_cmd_9x16)

    print("Video has been cropped and saved :)")

# Example usage
input_file = ctx.path
convert_video_to_social(input_file)