#! python3
from pathlib import Path, PurePath

from NYOR_Foundation import *

# -------------------------------------------------------------------------------
# NYOR / Nyor / N.Y.O.R. | Nuke Your Old Renders
#
# Deletes every render in your NukeStudio project except the one for the highest version of each comp.
#
# -------------------------------------------------------------------------------
# Tested:
# Python 3.6
# Nuke 11.1v4
#
# -------------------------------------------------------------------------------
# TODO:
# - Commandline interface: confirm project and files before deleting
# - Make Send2Trash optional
#
# -------------------------------------------------------------------------------

# -------------------------------------------------------------------------------
# Project Settings
# project_name: Name should be the same as project's folder name
# NS_folder: NukeStudio project root folder

film_projects = ProjectsLibrary("Filmes", "D:/Projetos/Ativos/Filmes")

project_name = "2018 Neptunea"
NS_folder = "VFX/NUKE"

project = Project(film_projects, project_name, NS_folder)

project.print_hierarchy()

