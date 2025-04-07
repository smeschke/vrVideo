import pandas as pd
import os
csv_file = [f for f in os.listdir() if f.endswith(".csv")][0]
df = pd.read_csv(csv_file)  

commands = []
project_name = "undef"

for _, row in df.iterrows():
    input_video = 'stitched/' + row[4]
    output_name = row[5]
    start_time = row[6]
    end_time = row[7]    
    if project_name == "undef": project_name = row[8]

    # Calculate fade-in and fade-out times
    fade_in_start = start_time
    fade_in_duration = 1  # 1 second fade-in
    fade_out_start = end_time - 1  # 1 second before the end
    fade_out_duration = 1  # 1 second fade-out
    fade_in_start = str(fade_in_start)
    fade_out_start = str(fade_out_start)

    # Generate the FFmpeg command with fade transitions
    command = (
        f"ffmpeg -i '{input_video}' -vf \"fade=t=in:st={fade_in_start}:d={fade_in_duration},"
        f"fade=t=out:st={fade_out_start}:d={fade_out_duration}\" "
        f"-ss {start_time} -to {end_time} '{output_name}.MP4'"
    )

    
    commands.append(command.strip())
    print(command)
    
# Save to a script file
with open("ffmpeg_trim_commands_"+project_name+".sh", "w") as script_file:
    script_file.write("\n\n".join(commands))


print("complete")
