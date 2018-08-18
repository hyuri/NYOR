#! python3
from pathlib import Path, PurePath
from itertools import groupby

# -------------------------------------------------------------------------------
# Path to NukeStudio Project Folder
NS_project_root = Path("D:/Projetos/Ativos/Filmes/2018 Neptunea/VFX/NUKE")
renders_folder = PurePath("nuke/renders")

if list(NS_project_root.glob("*.hrox")) == []:
	input("No NukeStudio Project File(.hox) found on this folder. Press Enter to continue anyway.")

# (!) Note: variable name(s) "shot"(s), here, is(are) a folder name(s), not the actual media file(s)
shots = [item for item in NS_project_root.iterdir() if item.is_dir()]

# -------------------------------------------------------------------------------

def get_highest_version_number(shot):
	try:
		highest_version_render = max(list((shot / renders_folder).glob(f"{shot.name}*comp_v[0-9][0-9]*.dpx")), key=lambda file: int(file.name[file.name.find("comp_v") + 6 : file.name.find(".", (file.name.find("comp_v") + 6))]))
	except ValueError:
		print("Value Error")
		return
	
	version_start = highest_version_render.name.find("_v") + 2
	version_end = highest_version_render.name.find(".", version_start)

	highest_version_number = highest_version_render.name[version_start:version_end]

	return highest_version_number

def get_highest_version_number_by_files(files):
	try:
		highest_version_render = max(files, key=lambda file: int(file.name[file.name.find("comp_v") + 6 : file.name.find(".", (file.name.find("comp_v") + 6))]))
	except ValueError:
		return

	version_start = highest_version_render.name.find("_v") + 2
	version_end = highest_version_render.name.find(".", version_start)

	highest_version_number = highest_version_render.name[version_start:version_end]

	return highest_version_number

# -------------------------------------------------------------------------------
# Removes render files of old versions of shots without a clip number.
def purge_old_single_clip_versions_renders(shot):
	highest_version_number = get_highest_version_number(shot)

	print(f"[!{highest_version_number[0]}][!{highest_version_number[1]}]")
	# old_renders = list((shot / renders_folder).glob(f"{shot.name}*comp_v[!{highest_version_number}]*.dpx*"))
	old_renders = list((shot / renders_folder).glob(f"{shot.name}*comp_v[!{highest_version_number[0]}][!{highest_version_number[1]}]*.dpx*"))
	# print(f"{shot.name}*comp_v{highest_version_number}*.dpx*")
	if old_renders != []:
		for file in old_renders:
			print("Removing:", file.name)
			# file.unlink()
			pass
	
	else:
		print(shot.name, "| No old renders to be removed for this shot.")

# Removes render files of old versions of shots containing a clip number.
def purge_old_multiclip_versions_renders(shot):
	multiple_clips = list((shot / renders_folder).glob(f"{shot.name}*comp_[0-9]_v*.dpx*"))
	multiple_clips += list((shot / renders_folder).glob(f"{shot.name}*comp_[0-9][0-9]_v*.dpx*"))

	for clip_number, frames in groupby(multiple_clips, lambda file: int(file.name[file.name.find("_comp_") + 6 : file.name.find("_v", (file.name.find("_comp_") + 6))])):
		frames = list(frames)
		clip_highest_version_number = get_highest_version_number_by_files(frames)

		print(f"SHOT: {shot.name}")
		print(f"CLIP: {clip_number}")
		print(f"HIGHEST CLIP VERSION: {clip_highest_version_number}")

		old_renders = list((shot / renders_folder).glob(f"{shot.name}*comp_[!{clip_number}]_v[!{clip_highest_version_number}]*.dpx*"))

		if old_renders != []:
			for file in old_renders:
				print("Removing:", file.name)
				# file.unlink()
		
		else:
			# print("No renders to be removed for this clip number.")
			pass

def purge_old_versions_renders(shot):
	purge_old_single_clip_versions_renders(shot)
	# purge_old_multiclip_versions_renders(shot)

# -------------------------------------------------------------------------------

for shot in shots:
	purge_old_versions_renders(shot)