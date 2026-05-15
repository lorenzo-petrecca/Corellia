![Status](https://img.shields.io/badge/status-experimental-orange)
![License](https://img.shields.io/badge/license-MIT-green)

# Corellia

- [What is Corellia](#what-is-corellia)
- [Why Corellia](#why-corellia)
- [Features](#features)
- [Installation](#installation)
- [Quick start](#quick-start)
- [Examples](#examples)
- [Documentation](#documentation)
- [Current status](#current-status)
- [License](#license)

## What is Corellia

Corellia provides a unified CLI workflow for Python project management.

Corellia orchestrates Python version management, virtual environments, dependencies, project scripts and packaging through a single configuration file.

Instead of manually coordinating tools such as:

- pyenv
- venv
- pip
- build
- git

Corellia provides a consistent project-oriented interface designed to simplify setup, synchronization and packaging workflows.

---

## Why Corellia

Python projects often evolve into fragmented workflows:

- Python versions are managed separately
- virtual environments are manually recreated
- dependencies drift across machines
- scripts are undocumented or inconsistent
- packaging metadata becomes duplicated
- build workflows differ between projects

Corellia centralizes these concerns into a single source of truth:

```toml
corellia.toml
```

This allows projects to remain **more reproducible**, **easier to synchronize**, and more consistent across development environments.

Corellia does not aim to replace tools like `pyenv`, `pip` or `venv`.
Instead, it orchestrates them through a unified workflow.

---

## Features

- Python version management integration (`pyenv`)
- automatic virtual environment management
- dependency synchronization
- project script management
- reproducible project configuration
- package build workflow
- structured project layouts
- framework-aware scaffolding (experimental)

---


## Installation

### Requirements
- Python 3.12+
- pyenv
- Git *(optional, but recommended)*


### Install from PyPI

```bash
pipx install corellia-cli
```

### Install from source

```bash
git clone https://github.com/lorenzo-petrecca/Corellia.git
cd Corellia
pipx install -e .
```

> [!WARNING]
> Corellia is currently under active development.
> Workflows and configuration structures may evolve between releases.


---

## Quick Start

### Create a project

```bash
core create
```

The command interactively generates a new project and creates:

- project structure
- virtual environment
- `corellia.toml`
- Git repository
- initial dependency setup

### Synchronize the environment

```bash
core sync
```

This command recreates the local project environment from the configuration declared inside `corellia.toml`.

### Add dependencies

```bash
core add <package>
```

Dependencies are tracked directly inside `corellia.toml`, for example:

```bash
core add requests
```

produces:

```toml
[dependencies]
requests = "2.32.3"
```

### Execute project scripts

```bash
core run check
```

Scripts are declared directly inside the configuration:

```toml
[scripts.check]
command = "python --version"
mode = "strict"
description = "Check Python environment"
```

You can list available scripts with:

```bash
core run --list
```


### Build a distributable package

```bash
core init-build
core build
```

Corellia generates a pyproject.toml artifact and builds the project using the standard Python packaging workflow.


---

## Examples 

### Workflow example

```bash
core create
core add requests
core sync
core run check
core init-build
core build
```

### Configuration example

```bash
# corellia.toml

[project]
name = "myproject"
version = "0.1.0"
python = "3.12.10"
category = "package"
description = "Example project"

[environment]
manager = "pyenv"
venv = ".venv"

[dependencies]
requests = "2.32.3"

[scripts.dev]
command = "python main.py"
mode = "strict"
description = "Run development script"
```

### Package project structure

```text
myproject/
├── .venv/
├── src/
│   └── myproject/
│       └── __init__.py
├── tests/
├── corellia.toml
├── README.md
└── .gitignore
```

---

## Documentation

Full documentation is available in the `/docs` directory.

> [!Warning]
> The documentation may not be fully up to date with the latest versions

---

## Current Status

Corellia is currently focused on stabilizing the core project workflow experience for the `package` category.

Some areas of the project are still considered experimental or only partially implemented.


> [!IMPORTANT] Partially Supported
> - `app` project workflows
> - `deploy` project workflows
> - framework-specific integrations
> - advanced build metadata generation

> [!CAUTION] Not Yet Supported
> - Windows support
> - dependency structure validation inside `corellia.toml`
> - standalone executable builds
> - advanced deployment workflows

> [!NOTE]
> The internal configuration model and project structure may continue to evolve during the current development phase.

---

## License

This project is licensed under the MIT License.

