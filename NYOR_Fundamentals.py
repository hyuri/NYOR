#! python3
from pathlib import Path, PurePath
from itertools import groupby
from send2trash import send2trash

# -------------------------------------------------------------------------------
# Utilities

def get_tag_value(file_name, tag_name, original_string=False):
	render_tag = NS_render_tags.tags[tag_name]

	start = file_name.find(render_tag["start_marker"])
	if start == -1:
		return {"error": "start_marker_not_found"}

	start += len(render_tag["start_marker"])
	end = file_name.find(render_tag["end_marker"], start)

	if end == -1:
		return {"error": "end_marker_not_found"}

	value = file_name[start:end]

	if not original_string:
		return {"value": int(value)}

	return {"value": value}

# Wrapper functions, for easier-to-understand usage
def get_comp_number(file_name, original_string=False):
	comp_number = get_tag_value(file_name, "comp_number", original_string)

	if "value" in comp_number:
		return comp_number["value"]

	if "error" in comp_number:
		if comp_number["error"] == "end_marker_not_found":
			return 1

		if comp_number["error"] == "start_marker_not_found":
			raise Exception("get_comp_number Error: start_marker not found.")

	else:
		raise Exception("get_comp_number Error: No keys found.")

def get_version_number(file_name, original_string=False):
	version_number = get_tag_value(file_name, "version_number", original_string)

	if "value" in version_number:
		return version_number["value"]

	if "error" in version_number:
		if version_number["error"] == "end_marker_not_found":
			raise Exception("get_version_number Error: end_marker not found.")

		if version_number["error"] == "start_marker_not_found":
			raise Exception("get_version_number Error: start_marker not found.")

	else:
		raise Exception("get_version_number Error: No keys found.")

def get_frame_number(file_name, original_string=False):
	frame_number = get_tag_value(file_name, "frame_number", original_string)

	if "value" in frame_number:
		return frame_number["value"]

	if "error" in frame_number:
		if frame_number["error"] == "end_marker_not_found":
			raise Exception("get_frame_number Error: end_marker not found.")

		if frame_number["error"] == "start_marker_not_found":
			raise Exception("get_frame_number Error: start_marker not found.")

	else:
		raise Exception("get_frame_number Error: No keys found.")

# -------------------------------------------------------------------------------

def get_frames(shot, comp_number, comp_version_number):
	render_files = list(shot.renders_path.glob(f"{shot.name}_comp_*.dpx"))
	counter = 0
	for render_comp_number, comp_files in groupby(render_files, lambda file: get_comp_number(file.name)):
		comp_files = sorted(comp_files, key=lambda file: get_comp_number(file.name))

		print("\n", "-"*30)
		print(f"{shot.name} | Comp Number: {comp_number} | Render Comp Number: {render_comp_number}")
		# print("Comp Files:", len(comp_files))

		if render_comp_number == comp_number:
			for render_version_number, version_files in groupby(comp_files, lambda file: get_version_number(file.name)):
				version_files = sorted(version_files, key=lambda frame_file: get_version_number(frame_file.name))

				if render_version_number == comp_version_number:
					print(f"MATCH | Render Version: {render_version_number} / Comp Version: {comp_version_number}")
					# print("Version Files:", len(version_files))
					return version_files

				else:
					print(f"NOT MATCH | Render Version: {render_version_number} / Comp Version: {comp_version_number}")
					return []
		
		else:
			pass
		# for index, comp_version in enumerate(comp_files):
		# 	print(index+1, comp_version)

		if counter == 1:
			assert False

		counter += 1

	# for file in render_files:
	# 	frames = Frame()
	pass

# -------------------------------------------------------------------------------
# Models

class RenderTagsCollection:
	def __init__(self, name):
		self.name = name
		self.tags = {}

	def add(self, name, start_marker, end_marker):
		if name in self.tags:
			raise Exception("This Tag is already in this collection.")
		
		self.tags[name] = {"start_marker": start_marker, "end_marker": end_marker}

	def dict_add(self, tags_dict):
		pass

	def __str__(self):
		return f"RenderTagsCollection: {str([render_tag for render_tag in self.tags])}"

class File:
	def __init__(self, path):
		self.path = Path(path)
		self.name = self.path.name

	def __str__(self):
		return f"File: {self.name}"

class Frame:
	def __init__(self, file):
		self.file = file
		self.string = get_tag_value(self.file.name, "frame_number", original_string=True)
		self.number = get_tag_value(self.file.name, "frame_number")

	def __str__(self):
		return str(f"Frame {self.string}")

class Render:
	def __init__(self, frames, extension="dpx"):
		self.frames = frames # [sorted_list_of_frames]
		self.extension = extension

	def delete(self):
		for frame in self.frames:
			# frame.unlink()
			send2trash(str(frame.resolve()))

# -------------------------------------------------------------------------------
# NukeStudio Render Tags Collection Setup

NS_render_tags = RenderTagsCollection("NS_render_tags")
NS_render_tags.add("comp_number", "_comp_", "_v")
NS_render_tags.add("version_number", "_v", ".")
NS_render_tags.add("frame_number", ".", ".")
