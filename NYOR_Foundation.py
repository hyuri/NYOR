#! python3
from pathlib import Path, PurePath
from itertools import groupby

from NYOR_Fundamentals import *

# -------------------------------------------------------------------------------
# Utilities

def get_shots(project):
	shots = [Shot(item) for item in project.path.iterdir() if item.is_dir()]

	return shots

def get_renders(shot):
	render_files = get_render_files(shot)

	renders = {}

	for render_comp_number, comp_files in groupby(render_files, lambda file: get_comp_number(file.name)):
		comp_files = sorted(comp_files, key=lambda file: get_comp_number(file.name))

		# comps = filter_by(render_files, "comp")
		# print(len(comps[0][1]), len(comp_files))
		# print(comps[0][1][0] == comp_files[0])
		# print(comps[0][1][0].name, comp_files[0].name, sep="\n")

		versions = {}

		for render_version_number, version_files in groupby(comp_files, lambda file: get_version_number(file.name)):
			version_files = sorted(version_files, key=lambda frame_file: get_version_number(frame_file.name))

			render = Render(version_files)
			version = Version(render_version_number, render)

			versions[render_version_number] = version

		renders[render_comp_number] = versions

	return renders

def get_comps(shot):
	renders = get_renders(shot)
	comps_files = get_comps_files(shot)

	comps = []

	for comp_number, comp_versions in groupby(comps_files, lambda file: get_comp_number(file.name)):
		comp_versions = sorted(comp_versions, key=lambda version_file: get_version_number(version_file.name))
		
		comp_renders = renders.get(comp_number)

		versions = {}

		for comp_version in comp_versions:
			version_number = get_version_number(comp_version.name)

			if (comp_renders != None) and (comp_renders.get(version_number) != None):
				versions[version_number] = comp_renders.get(version_number)
				continue

			versions[version_number] = Version(version_number, None)

		comp = Comp(comp_number, versions)
		comps.append(comp)

	return sorted(comps, key=lambda comp: comp.number)

# -------------------------------------------------------------------------------
# Models

class Version:
	def __init__(self, number, render=None):
		self.number = number # Think about adding auto-incrementing option
		self.render = render

	def delete_render(self):
		self.render.delete()

	def __str__(self):
		return f"Version: {self.number}"

class Comp:
	def __init__(self, number, versions):
		self.number = number
		self.versions = versions

	def get_highest_version(self):
		# return max(self.versions).number
		pass

	def get_number_of_versions(self):
		return len(self.versions)

	def delete_version(self, version_number):
		self.versions[version_number].delete_render()
		del self.versions[version_number]

	def delete_old_versions(self):
		for version in self.versions:
			# print(version.render)

			if version.number < self.get_highest_version():
				self.delete_version(version.number)

			else:
				pass

	def add_new_version(self, version_number):
		# Should scan through the folder for files (glob?)
		# and return some kind of error or message if version is not found on disk
		# Path.exists()

		# if version_number not in self.versions:
		# 	new_render = Render(frames=???)
		# 	new_version = Version(version_number, new_render)
		# 	self.versions[version_number] = new_version
		
		pass

	def scan_for_new_versions(self):
		pass

	def update_versions(self):
		pass

	def __str__(self):
		return f"Comp: {self.number}"

class Shot:
	def __init__(self, path, comps_path=None, renders_path=None):
		self.path = path
		self.name = self.path.name
		self.comps_path = self.path/"nuke"/"script"
		self.renders_path = self.path/"nuke"/"renders"
		
		self.comps = get_comps(self)

		# Setting up available comps
		# self.comps = [Comp(path=shot_path) for shot_path in self.path]
		
		# for index, comp in enumerate(self.comps):
		# 	# print(index+1, "| comp:", comp)

	def scan_for_new_comps(self):
		pass

	def update_comps(self):
		pass

	def delete_orfan_renders(self):
		pass

	def __str__(self):
		return f"Shot: {self.name}"

	def __repr__(self):
		return f"Shot: {self.name}"

class Project:
	def __init__(self, library, name, NS_folder):
		self.library = library
		self.name = name
		self.path = self.library.path/self.name/NS_folder

		if list(self.path.glob("*.hrox")) == []:
			input("No NukeStudio Project File(.hox) found on this folder. Press Enter to continue anyway.")
		
		self.shots = get_shots(self)

	def print_hierarchy(self):
		print(f"{self} ({len(self.shots)} shots)", "\n")
		for shot in self.shots:
			print(f"{shot} ({len(shot.comps)} comps)")
			
			for comp in shot.comps:
				print(f"  |_ {comp} ({len(comp.versions)} versions)")
				
				for version in comp.versions:
					print(f"    |_ {comp.versions[version]} | Render: {comp.versions[version].render}")

			print("\n")

	def __str__(self):
		return f"Project: {self.name}"

class ProjectsLibrary:
	def __init__(self, name, path):
		self.path = Path(path)
		self.name = name

	def __str__(self):
		return f"Project Library: {self.name}"