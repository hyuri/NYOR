#! python3
from pathlib import Path, PurePath
from itertools import groupby

from NYOR_Fundamentals import *

# -------------------------------------------------------------------------------
# Utilities

def get_shots(project):
	shots = [Shot(item) for item in project.path.iterdir() if item.is_dir()]

	return shots

def get_comps(shot):
	comps_files = list(shot.comps_path.glob(f"{shot.name}_comp_*.nk"))

	comps = []

	for comp_number, comp_versions in groupby(comps_files, lambda file: get_comp_number(file.name)):
		comp_versions = sorted(comp_versions, key=lambda version_file: get_version_number(version_file.name))

		# for version in comp_versions:
		# 	version_number = get_version_number(version.name)

		# print("New Comp: ", comp_number)
		# print(str([comp_file.name for comp_file in comp_versions]))

		versions = {}
		for comp_version in comp_versions:
			version_number = get_version_number(comp_version.name)

			render = Render(get_frames(shot, comp_number, version_number))
			version = Version(version_number, render)

			versions[version.number] = version

		comp = Comp(comp_number, versions)
		comps.append(comp)

	return sorted(comps, key=lambda comp: comp.number)

# -------------------------------------------------------------------------------
# Models

class Version:
	def __init__(self, number, render):
		self.number = number # Think about adding auto-incrementing option
		self.render = render # Render()

	def delete_render(self):
		self.render.delete()

	# def __str__(self):
	# 	return f"Version: {self.number}"

class Comp:
	def __init__(self, number, versions):
		self.number = number
		self.versions = {} #{version.number: version for version in versions} # {1: Version(), 2: Version() }

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

	def scan_for_new_versions(self, add_new=True):
		if add_new:
			# self.add_new_version(version_number)
			pass
		pass

	# def __str__(self):
	# 	return f"comp: {self.number}"

class Shot:
	def __init__(self, path, renders_path=None):
		self.path = path
		self.name = self.path.name
		self.comps_path = self.path/"nuke"/"script"
		self.renders_path = self.path/"nuke"/"renders"
		
		self.comps = get_comps(self)

		# Setting up available comps
		# self.comps = [Comp(path=shot_path) for shot_path in self.path]
		
		# for index, comp in enumerate(self.comps):
		# 	# print(index+1, "| comp:", comp)

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

		# Setting up available shots
		self.shots = get_shots(self)

		for index, shot in enumerate(self.shots):
			# print(index+1, "| comps:", shot.comps)
			# print(shot.comps)
			pass

	def __str__(self):
		return f"(Project) {self.name}"

class ProjectsLibrary:
	def __init__(self, name, path):
		self.path = Path(path)
		self.name = name

	def __str__(self):
		return f"(Project Library) {self.name}"

# -------------------------------------------------------------------------------
# Project Settings

film_projects = ProjectsLibrary("Filmes", "D:/Projetos/Ativos/Filmes")

# Should be the same as project's root folder
project_name = "2018 Neptunea"
NS_folder = "VFX/NUKE"

project = Project(film_projects, project_name, NS_folder)

print(len(project.shots))
for shot in project.shots:
	print(f"shot: {shot.name} ({len(shot.comps)} comps)")
	for comp in shot.comps:
		print("comp:", comp.number)

# for frame in list_of_frames:
# 	if file is