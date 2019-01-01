#! python3
from pathlib import Path, PurePath

from NYOR_Foundation import *

# -------------------------------------------------------------------------------
# NYOR / Nyor / N.Y.O.R. | Nuke Your Old Renders
# Deletes every render(and .tmp files) in your NukeStudio project except the one for the highest version of each comp.
# -------------------------------------------------------------------------------
# Tested:
# Python 3.6
# Nuke 11.1v4
# -------------------------------------------------------------------------------
# TODO:
# - Add logging
# -------------------------------------------------------------------------------

# -------------------------------------------------------------------------------
# Project Settings
# project_name: Name should be the same as project's folder name
# NS_folder: NukeStudio project root folder

film_projects = ProjectsLibrary("Filmes", "D:/Projetos/Ativos/Filmes")

project_folder = "2018 Neptunea"
NS_folder = "VFX/NUKE"

# -------------------------------------------------------------------------------
# Operations

aum_vfx = Project(film_projects, project_folder, NS_folder)

options = {
			1: {
				"title": "Print Hierarchy",
				"uid": "print_hierarchy",
				"command": aum_vfx.print_hierarchy
			},
			2: {
				"title": "Delete Renders of Old Versions",
				"uid": "del_all_renders_old_versions",
				"command": aum_vfx.delete_renders_of_older_versions # send_to_trash is set to "True" by default.
			},
			3: {
				"title": "Delete Tmp Render Files",
				"uid": "del_all_render_tmp_files",
				"command": aum_vfx.delete_render_tmp_files # send_to_trash is set to "True" by default.
			},
			4: {
				"title": "Delete Renders of Latest Version",
				"uid": "del_all_renders_latest_version",
				"command": aum_vfx.delete_renders_of_latest_version # send_to_trash is set to "True" by default.
			},
			5: {
				"title": "Exit.",
				"uid": "exit",
				"command": exit
			}
		}

def print_options():
		print("-"*30)
		print("OPTIONS:")
		for option in options:
			print(option, options[option]["title"])
		print("\n")

while True:
	print_options()

	try:
		user_choice = int(input("Choose a number and press Enter.\n"))

		if (options[user_choice]["uid"] == "del_all_renders_old_versions") or (options[user_choice]["uid"] == "del_all_render_tmp_files"):
			confirmation = input(f"{options[user_choice]['title']}. Are you sure?\n(Type Yes to confirm and press Enter.)\n")

			if confirmation in ["Yes", "yes", "YES", "y"]:
				try:
					options[user_choice]["command"]()
				except PermissionError:
					print("\n {{{ (!) PermissionError. A program might have this file open. }}}\n")
				
				continue

		options[user_choice]["command"]()
	
	except (KeyError, ValueError):
		print("\n {{{ (!) Invalid option. Try again! }}}\n")