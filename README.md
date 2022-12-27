
<div align="center">

# 📦 Game 3D Toolkit

![license](https://img.shields.io/badge/license-MIT-green?logo=open-source-initiative&logoColor=white)

A package that contains a variety of tools for working with 3D models in the context of game development.

</div>

## Installation

To install `game_3d_toolkit`, run the following command
```
pip install git+https://github.com/MechanicalFlower/game-3d-toolkit.git
```

## Usage

### As a Python package

```
import game_3d_toolkit

# Your code here
```

### As a script

Scripts are defined in the poetry configuration file.

To use `game_3d_toolkit` scripts, run the following command:
```
poetry run script_name [arguments]
```

For example, to use the optimize-models script:
```
poetry run optimize-models [arguments]
```

For more information about the available arguments and options for a specific script, run the following command:
```
poetry run script_name --help
```

For example, to get help for the optimize-models script:
```
poetry run optimize-models --help
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

### Prerequisites

To set up the local development environment for game_3d_toolkit, you will need to install Poetry.

### Setting up the local development environment

To set up the local development environment for game_3d_toolkit, follow these steps:

1. Clone the repository:
```
git clone https://github.com/MechanicalFlower/game_3d_toolkit.git
```

2. Navigate to the repository directory:
```
cd game_3d_toolkit
```

3. Install the dependencies:
```
poetry install
```

This will also install pre-commit, which is used to automatically run checks and formatting on the code before commits.
