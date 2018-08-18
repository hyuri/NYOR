#! python3
from pathlib import Path, PurePath

from NYOR_Foundation import *

# NYOR / Nyor / N.Y.O.R. | Nuke Your Old Renders
# Deletes every render in your NukeStudio project except the one for your highest version.

# -------------------------------------------------------------------------------
frame_file = File(path=f"{projects_folder}/{project_folder}/{NS_folder}/WARP/nuke/renders/WARP_comp_2_v01.0181.dpx")
frame = Frame(frame_file)

comp_number = get_comp_number(frame.file.name)
version_number = get_version_number(frame.file.name)
frame_number = get_frame_number(frame.file.name, original_string=True)

print(frame.file.name)
print(comp_number, version_number, frame_number)

# Project & Shots Setup
# project = Project(path=f"{projects_folder}/{project_folder}/{NS_folder}")

# shots = []

# for shot in shots_folders:
# 	new_shot = Shot(path=project_root / shot, name=shot, )
# 	shots.append(new_shot)

# for frame in list_of_frames:
# 	if file is

# Commandline interface: confirm project and files before deleting

# Make Send2Trash optional