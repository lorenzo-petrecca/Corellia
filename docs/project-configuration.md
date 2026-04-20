# Project Configuration

## Overview

Every Corellia project is configured through a single file:

`corellia.toml`

This file acts as the **single source of truth** for the entire project.

It defines:

- project metadata
- Python version
- project category
- dependencies
- scripts
- optional framework configuration

All Corellia commands operate based on this file.

---

## File Structure

A typical corellia.toml looks like this:

```toml
[project]
name = "myproject"
version = "0.1.0"
python = "3.12"
category = "package"

[environment]
manager = "pyenv"
venv = ".venv"

[framework]
name = "none"

[dependencies]
requests = "2.32.3"

[dev-dependencies]
pytest = "8.3.0"

[scripts.dev]
command = "python main.py"
mode = "strict"
description = "Run development server"
```

### `[project]`

Defines the core metadata of the project.

#### Fields

`name`
The project name.
Used for:

- directory naming
- package naming (for package category)
- build artifacts

`version`
The project version.
Used for:

- build artifacts (dist/)
- generated pyproject.toml
- package metadata

`python`
The Python version required for the project.
Corellia will ensure this version is available via `pyenv` ans bind it locally to the project

`category`
Defines the type of project.
Supported values:

- package → reusable Python package
- app → executable application
- deploy → deployment-oriented project

The category affects:

- project structure
- available commands
- build support

<br/>

### `[environment]`

Defines how the project environment is managed.

#### Fields

`manager`
Currently supported:

```toml
manager = "pyenv"
```

Used to manage Python versions.

`venv`
Name of the virtual environment directory.

```toml
venv = ".venv"
```

Corellia will create and reuse this environment automatically.

<br/>

### `[framework]`

Defines the optional framework used by the project.

#### Fields

`name`
Supported values:

- none
- django

If a framework is selected, Corellia may:

- install additional dependencies
- generate project files
- define default scripts

<br/>

### `[dependencies]`

Defines runtime dependencies.

Format:

```toml
[dependencies]
package_name = "version"
```

Example:

```toml
[dependencies]
requests = "2.32.3"
rich = "13.7.0"
```

Corellia will:

- install these dependencies via `pip`
- enforce exact versions

*Dependencies must be defined using exact versions.
Corellia currently requires pinned versions to ensure deterministic environments.*

<br/>

### `[dev-dependencies]`

Defines development-only dependencies.

Example:

```toml
[dev-dependencies]
pytest = "8.3.0"
black = "24.3.0"
```

These are installed during:

```bash
core sync
```

Unless explicitly disabled.

<br/>

### `[scripts.<name>]`

Defines executable project scripts.

Each script is defined as a table:

```toml
[scripts.<name>]
command = "<command>"
mode = "<mode>"
description = "<optional>"
```

#### Fields

`command`
The command to execute.
Example:

```toml
command = "python main.py"
```

`mode`
Defines how the command is executed.
Supported modes:

- `strict` → executed directly (recommended)
- `shell` → executed through a shell


`description` *(optional)*
Human-readable description of the script.


Example

```toml
[scripts.dev]
command = "python main.py"
mode = "strict"
description = "Run development server"

[scripts.test]
command = "pytest"
mode = "shell"
description = "Run tests"
```

---

## How Configuration is Used

Corellia reads `corellia.toml` and:

- prepares the Python environment
- installs dependencies
- executes scripts
- generates build configuration (`pyproject.toml`)
- determines project structure

The file is never partially applied, changes always affect the entire project behavior

---

## Derived Configuration

Some files are generated automatically from `corellia.toml`.

- `pyproject.toml`
    Generated with:

    ```bash
    core init-build
    ```

    Used for:
    - packaging
    - distribution
    - build tools

--- 

## Best Practices

### Use scripts for common tasks

Define frequently used commands as scripts instead of running them manually.

```bash
core run dev
```

### Keep configuration centralized

All project configuration should be defined in `corellia.toml`.
Avoid duplicating configuration across multiple files.

### Avoid modifying generated files unnecessarily

Generated files should generally not be modified manually.
Corellia manages files such as:

- `.venv/`
- `pyproject.toml`

However, minor adjustments may be applied when necessary, for example adding a project description to `pyproject.toml`

Be aware that manually edited files may be overwritten by future Corellia operations.


<!-- ---

## Next Steps
- Learn how project types work in **Categories**
- Explore available commands in **Commands**
- Understand packaging in **Build & Packaging** -->