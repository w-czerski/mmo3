# MMO3 Manifest Manager

`mmo3` is a simple command-line tool built to manage O3DE (`Open 3D Engine`) manifests for projects and engines. If you're working with multiple versions of O3DE engines and their respective manifests, `mmo3` allows you to effortlessly switch between them, create new manifest configurations, and manage project setups without manually copying files.

### Why This Tool?
O3DE configurations are stored in JSON files (e.g., `o3de_manifest.json`), and it's often necessary to use different engine versions, project setups, or attached gems—all of which may require different manifests. `MMO3` simplifies the process of switching between and managing these manifests stored in `~/.o3de`.

---

## Features

- **List available manifests**: List all stored manifest files within the `~/.manifests` folder.
- **Set active manifest**: Switch the active `o3de_manifest.json` by copying a stored manifest to the required location (`~/.o3de/o3de_manifest.json`).
- **Create new manifests**: Generate new placeholder manifests that you can customize.
- **Open manifests**: Open any manifest directly in a text editor (defaults to `nano` but can be customized to another editor like `vim` or `code`).
- **Duplicate existing manifests**: Easily duplicate an existing manifest and give it a new name.
- **Version checking**: Quickly check the version of the `mmo3` tool installed.

---

## Installation Instructions

1. **Clone this repository**:
```bash
   git clone https://github.com/wc-robotec/mmo3.git
   cd mmo3
```

2. **Run the installation script :**
```bash
./install.sh
```
This will check for the ~/manifests directory and create it if necessary. It will then copy the mmo3.py script to /usr/local/bin/ for global access and set the appropriate executable permissions.     

3. **Custom Installation Path**

If you want to install the `mmo3` script to a custom location (for example, if you don't have root permissions to write into `/usr/local/bin/`), specify your desired installation path as an argument to the installation script: 
```bash
./install.sh /your/custom/directory
```

Ensure that the specified installation path (e.g., `/your/custom/directory`) is added to your `$PATH`. For example, you can add it to your .bashrc or .zshrc: 
```bash
export PATH=$PATH:/your/custom/directory
```

Remember to source your configuration file: 
```bash
source ~/.bashrc  # or source ~/.zshrc
```

---

## How to Use 

The simplest way to start using `mmo3` is by running `mmo3 -h` to check available commands: 
```bash
mmo3 -h
```

### Available Commands: 

- **List all manifests :** 
```bash
mmo3 -list    # or mmo3 -ls
```
This will display all the manifest files stored in `~/.manifests`. 

- **Set an active manifest :** 
```bash
mmo3 -set engine_v2.json
```
Copies engine_v2.json from `~/.manifests` to `~/.o3de/o3de_manifest.json`, making it the currently active manifest. 

- **Create a new manifest :** 
```bash
mmo3 -new my_new_manifest.json
```
Creates a new manifest file with some defaults in the `~/.manifests` directory. 

- **Open a manifest (default nano) :** 
```bash
mmo3 -open engine_v1.json
```
This opens the specified manifest directly in nano for editing. If no specific manifest is provided, it will open the currently active one located in `~/.o3de/o3de_manifest.json`. 

- **Duplicate a manifest :** 
```bash
mmo3 -duplicate engine_v1.json
```
Duplicates an existing manifest and lets the user name the duplicated file. 

- **Check the version :** 
```bash
mmo3 -version
```

---

## Example Workflow 
1. **List all manifests** when working on multiple projects: 
```bash
mmo3 -ls
```
2. **Set an active manifest** for project work: 
```bash
mmo3 -set my_project_manifest.json
```
3. **Create a new manifest** for a new project you're working on: 
```bash
mmo3 -n new_project_manifest.json
```

---

## How It Works 

`mmo3.py` manages the `o3de_manifest.json` required by Open 3D Engine (O3DE). It works by copying and replacing the manifest located at `~/.o3de/o3de_manifest.json` with the JSON files stored in a separate directory (`~/manifests`). 

Here’s a breakdown of the basic functionality: 

- **Command-line arguments :** The script takes arguments (like `-list`, `-set`, `-new`) to instruct what action to perform.
- **Manifest directory management :** Manifests are stored locally in `~/.manifests`. These can be selected, created, and duplicated without manual file copying or renaming.
- **Active manifest :** The active manifest file resides in `~/.o3de/o3de_manifest.json`, replaced as needed when you switch between different configurations.

The tool is designed to streamline development across different engine versions, projects, and attached gems, by allowing quick swaps of configuration files. 

---

## Requirements
    Python 3.x
    Linux/Ubuntu (though should work on other UNIX-like systems)
---

## License 

**GNU GENERAL PUBLIC LICENSE.**

Everyone is permitted to copy and distribute verbatim copies
of this license document, but changing it is not allowed.

---

## Contributing
Have ideas for features? Found a bug? Feel free to open an issue or submit a pull request! 
