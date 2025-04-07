import pandas as pd
import os
import shlex

# Load CSV
csv_file = [f for f in os.listdir() if f.endswith(".csv")][0]
df = pd.read_csv(csv_file)
project_name = "undef"

commands = []

for _, row in df.iterrows():
    left_file = row[0]
    right_file = row[2]
    left_key = row[1]
    right_key = row[3]
    delta_key = int(right_key - left_key)

    if project_name == "undef":
        project_name = row[8]

    left_input = f"left/{left_file}"
    right_input = f"right/{right_file}"

    output_filename = f"{left_file.split('.')[0]}_{right_file.split('.')[0]}_stitched.MP4"

    if delta_key >= 0:
        # Right video delayed, left starts earlier → use left audio (input 0)
        filter_complex = f"[1:v]select=gte(n\\,{delta_key}),setpts=PTS-STARTPTS[right]; [0:v][right]hstack"
        audio_map = "-map 0:a"
    else:
        # Left video delayed, right starts earlier → use right audio (input 1)
        filter_complex = f"[0:v]select=gte(n\\,{abs(delta_key)}),setpts=PTS-STARTPTS[left]; [1:v][left]hstack"
        audio_map = "-map 1:a"

    cmd = (
        f'ffmpeg -i {shlex.quote(left_input)} -i {shlex.quote(right_input)} '
        f'-filter_complex "{filter_complex}" '
        f'-map "[v]" {audio_map} -shortest -y {shlex.quote(output_filename)}'
    ).replace('hstack', 'hstack[v]')  # Label the output video stream

    commands.append(cmd)

# Write to shell script
with open(f"ffmpeg_stitch_commands_{project_name}.sh", "w") as script_file:
    script_file.write("\n\n".join(commands))

print("complete")
