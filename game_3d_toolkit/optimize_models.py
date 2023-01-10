"""
This script is designed to optimize 3D models in a specified directory, and store the optimized models in a separate
output directory. It is intended to be used as a tool for optimizing 3D models to improve their performance and reduce
their file size.

The script requires the 'gltfpack' command-line tool to be installed and available in the system PATH.
It can process 3D models in the GLTF, GLB, and OBJ formats.
If the script encounters a gLTF file with errors, it will attempt to fix the errors using Blender.
Therefore, the script also requires Blender to be installed and available in the system PATH.

To use the script, pass the directory containing the 3D models to optimize as the first argument.
Use the '--output-directory' flag to specify a separate directory to store the optimized 3D models.
Use the '--no-fix' flag to skip the step of fixing gLTF files with errors.
Use the '--replace' flag to replace the original 3D model with the optimized version.

Examples:
    python optimize_models.py /path/to/directory --fix-model --output-directory /path/to/output/directory
    python optimize_models.py /path/to/directory --no-fix --replace
"""

import argparse
import re
import subprocess
from pathlib import Path
from typing import Optional

import bpy
from tqdm import tqdm


def optimize_models(directory: Path, *, output_directory: Optional[Path] = None, fix: bool, replace: bool) -> None:
    """
    Optimize 3D models in the specified directory, and store the optimized models in the specified output directory.

    Parameters:
        directory (Path): The directory containing the 3D models to optimize.
        output_directory (Path): The directory to store the optimized 3D models.
        fix (bool): Flag indicating whether to fix gLTF files with errors.
        replace (bool): Flag indicating whether to replace the original 3D models with the optimized versions.
    """
    # Compile the regular expression
    pattern = re.compile(r"^(?!.*(optimized|fixed)).*\.(glb|obj|gltf)$")

    # Generate a list of Path objects
    model_files = [path for path in directory.rglob("*.*") if pattern.match(path.name)]

    for model_file in tqdm(model_files):
        # Determine the input path
        if fix:
            # Clean the input model
            input_path = fix_model(model_file)
        else:
            input_path = model_file

        # Determine the output path
        if output_directory:
            output_path = Path(output_directory, model_file.name).with_suffix(".glb")
        else:
            if replace:
                output_path = model_file.with_suffix(".glb")
            else:
                output_path = model_file.with_name("optimized_" + model_file.name).with_suffix(".glb")

        # Build the Meshoptimizer command
        command = ["gltfpack", "-cc", "-i", str(input_path), "-o", str(output_path)]

        # Run Meshoptimizer to optimize the model
        subprocess.run(command, shell=True, stderr=subprocess.STDOUT)


def fix_model(model_file: Path) -> Path:
    """
    Fix any errors in the given gLTF or GLB file by importing and exporting it with Blender.

    Parameters:
        model_file (Path): The path to the gLTF or GLB file to fix.

    Returns:
        Path: The path to the fixed version of the file.
    """
    # Check if the file is already fixed, or if it is not a gLTF or GLB file
    if "fixed" not in model_file.name and model_file.suffix in (".gltf", ".glb"):
        output_file = model_file.with_name("fixed_" + model_file.name)

        # Import the GLTF file
        bpy.ops.import_scene.gltf(filepath=str(model_file))

        # Export the GLTF file
        bpy.ops.export_scene.gltf(filepath=str(output_file))

        # Return the fixed version of the file
        return output_file

    # Return the original file
    return model_file


def cli():
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", help="directory containing the 3D models to optimize")
    parser.add_argument("--output-directory", help="directory to store the optimized 3D models", default=None)
    parser.add_argument("--no-fix", action="store_true", help="skip the step of fixing gLTF files with errors")
    parser.add_argument(
        "--replace", action="store_true", help="replace the original 3D models with the optimized versions"
    )
    args = parser.parse_args()

    output_directory = Path(args.output_directory) if args.output_directory else None

    # Optimize models in the specified directory
    optimize_models(
        Path(args.directory), output_directory=output_directory, fix=(not args.no_fix), replace=args.replace
    )


if __name__ == "__main__":
    cli()
