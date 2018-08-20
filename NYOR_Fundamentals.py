#! python3
from pathlib import Path, PurePath
from itertools import groupby
from send2trash import send2trash

# -------------------------------------------------------------------------------
# Utilities

def get_tag_value(file_name, tag_name, original_string=False):
	render_tag = NS_render_settings.tags[tag_name]

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

def get_comps_files(shot):
	comps_files = list(shot.comps_path.glob(f"{shot.name}_comp_*.nk"))

	return comps_files

def get_render_files(shot, extension="dpx"):
	'''
		Arguments: shot, extension

		Valid "extension" values(default: "dpx"):
			"<file_ext>"
			"all"
	'''

	if (extension not in NS_render_settings.extensions) and (extension != "all"):
		raise Exception(f"get_render_files Error: Unknown file extension '{extension}'.")
	
	if extension == "all":
		render_files = []
		
		for extension in NS_render_settings.extensions:
			render_files.append(list(shot.renders_path.glob(f"{shot.name}_comp_*.{extension}")))

		return render_files
	
	render_files = list(shot.renders_path.glob(f"{shot.name}_comp_*.{extension}"))

	return render_files

# -------------------------------------------------------------------------------

def filter_by(element, filter_type):
	'''
		Possible filter types: "comp"; "version"
		"comp": should be applied to an 'element' that is a regular list of paths.
		"version": should be applied to an 'element' that is a regular list of paths.
	'''
	if filter_type == "comp":
		comps = []
		for comp_number, comp_files in groupby(element, lambda file: get_comp_number(file.name)):
			comp_files = sorted(comp_files, key=lambda file: get_comp_number(file.name))

			comps.append((comp_number, comp_files))

		return comps

	if filter_type == "version":
		versions = []
		for version_number, version_files in groupby(element[1], lambda file: get_version_number(file.name)):
			version_files = sorted(version_files, key=lambda file: get_version_number(file.name))

			versions.append((version_number, version_files))

		return versions

	else:
		raise Exception(f"filter_by Error: Invalid filter type '{filter_type}'.")

# -------------------------------------------------------------------------------
# Models

class RenderSettings:
	def __init__(self, name):
		self.name = name
		self.tags = {}
		self.extensions = []

	def add_tag(self, name, start_marker, end_marker):
		if name in self.tags:
			raise Exception(f"RenderSettings.add_tag Error: Tag '{name}' is already in the settings.")
		
		self.tags[name] = {"start_marker": start_marker, "end_marker": end_marker}

	def add_extension(self, extension):
		if extension in self.extensions:
			raise Exception(f"RenderSettings.add_extension Error: Extension '{extension}' is already in the settings.")
		
		self.extensions.append(extension)

	def list_extensions(self):
		pass

	def __str__(self):
		return f"RenderSettings: {self.name}"

# class File:
# 	def __init__(self, path):
# 		self.path = Path(path)
# 		self.name = self.path.name

# 	def __str__(self):
# 		return f"File: {self.name}"

# class Frame:
# 	def __init__(self, file):
# 		self.file = file
# 		self.string = get_tag_value(self.file.name, "frame_number", original_string=True)
# 		self.number = get_tag_value(self.file.name, "frame_number")

# 	def __str__(self):
# 		return str(f"Frame {self.string}")

class Render:
	def __init__(self, frames, extension="dpx"):
		self.frames = frames # [sorted_list_of_frames]
		self.extension = extension

	def delete(self):
		for frame in self.frames:
			# frame.unlink()
			# send2trash(str(frame.resolve()))
			# print("Frame Deleted.")
			pass

	def __str__(self):
		return f"Render ({len(self.frames)} frames)"

# -------------------------------------------------------------------------------
# NukeStudio RenderSettings setup

NS_render_settings = RenderSettings("NS_render_settings")

NS_render_settings.add_extension("dpx")

NS_render_settings.add_tag("comp_number", "_comp_", "_v")
NS_render_settings.add_tag("version_number", "_v", ".")
NS_render_settings.add_tag("frame_number", ".", ".")