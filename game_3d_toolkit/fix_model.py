"""
This script is designed to fix errors in gLTF files by importing and exporting them with Blender. It is intended to be
used as a tool for repairing gLTF files that may not be processed correctly by other tools due to errors.

To use the script, pass the path to the gLTF file to fix as the first argument.
The script will import the gLTF file, then export it as a new gLTF file with the name 'fixed_[original_name]'.

Example:
    blender.exe --background --python fix_model.py -- /path/to/file.gltf
"""

import argparse
import sys
from pathlib import Path

import bpy

argv = sys.argv
argv = argv[argv.index("--") + 1 :]

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("file")
args = parser.parse_args(argv)

gltf_file = Path(args.file)

# Import the GLTF file
bpy.ops.import_scene.gltf(filepath=str(gltf_file))

# Export the GLTF file
bpy.ops.export_scene.gltf(filepath=str(gltf_file.with_name("fixed_" + gltf_file.name)))
