#! python3
from pathlib import Path, PurePath

from NYOR_Foundation import *

# -------------------------------------------------------------------------------
# NYOR / Nyor / N.Y.O.R. | Nuke Your Old Renders
# Deletes every render in your NukeStudio project except the one for the highest version of each comp.
# -------------------------------------------------------------------------------
# Tested:
# Python 3.6
# Nuke 11.1v4
# -------------------------------------------------------------------------------
# TODO:
# - Add logging
# - Commandline interface: confirm project and files before deleting
# - Make Send2Trash optional
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

# aum_vfx.print_hierarchy()

aum_vfx.delete_renders_of_older_versions()