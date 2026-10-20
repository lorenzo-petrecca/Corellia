# Commands

## Overview

Corellia provides a set of commands to manage the entire lifecycle of a project.

| Command           | Description                              |
| ----------------- | ---------------------------------------- |
| `core create`     | Create a new project                     |
| `core sync`       | Synchronize environment and dependencies |
| `core add`        | Add a dependency                         |
| `core remove`     | Remove a dependency                      |
| `core run`        | Execute a project script                 |
| `core info`       | Show project information                 |
| `core init-build` | Initialize packaging configuration       |
| `core build`      | Build a distributable package            |
| `core version`    | Show or change the project version       |
| `core module rename` | Rename the main Python module        |


All commands operate based on the current project directory and its `corellia.toml`.


---

## `core create`

### Overview

Creates a new Corellia project.

This command initializes:

- project structure
- configuration file
- Python environment
- dependencies
- optional framework
- category-specific layout

The project structure is automatically generated based on the selected category and framework.

### Syntax

```bash
core create [name]
```

If `name` is not provided, Corellia will prompt for it interactively.

### Interactive Setup

Corellia will ask for:

- project name
- Python version
- category (`package`, `app`, `deploy`)
- framework (`none`, `django`)

### What It Does

The command performs the following steps:

1. creates the project directory
2. generates `corellia.toml`
3. resolves framework dependencies
4. sets local Python version using `pyenv`
5. creates the virtual environment (`.venv`)
6. upgrades `pip`
7. installs dependencies and dev-dependencies
8. bootstraps the selected framework
9. scaffolds the project based on category and sets the default `[project].module`
10. creates `.gitignore`
11. initializes a Git repository (if available)

### Example
```bash
core create myproject
```

### Notes

- The command is **interactive by default**
- All configuration is stored in `corellia.toml`
- The environment is fully prepared after creation
- The project is immediately ready to use

### Result

After running the command, the project directory will contain:

- `corellia.toml`
- `.venv/`
- category-specific files
- optional framework files
- `.gitignore`
- optional Git repository


---


## `core sync`

### Overview
Synchronizes the project environment with the configuration defined in `corellia.toml`.

This command ensures that:

- the correct Python version is active
- the virtual environment exists and is ready
- dependencies are installed and up to date

### Syntax

```bash
core sync [options]
```

### Options
`--clean`
Recreates the virtual environment from scratch.

```bash
core sync --clean
```

Behavior:

- removes the existing virtual environment
- creates a new one
- reinstalls all dependencies

`--no-dev`
Installs only runtime dependencies.

```bash
core sync --no-dev
```

Behavior:

- installs `[dependencies]`
- skips `[dev-dependencies]`

`--package <name>`

Installs or updates a single dependency.

```bash
core sync --package requests
```

Behavior:

- installs only the specified package
- must exist in corellia.toml


### Constraints

The following combinations are **not allowed**:

- `--clean` with `--package`
- `--no-dev` with `--package`


### What It Does

The command performs the following steps:

1. ensures the correct Python version is available
2. verifies or creates the virtual environment
3. upgrades `pip`
4. installs runtime dependencies
5. installs development dependencies (unless `--no-dev`)

If `--clean` is used the environment is rebuilt from scratch.


### Notes
- This is the primary command to apply changes from `corellia.toml`
- It should be run after modifying dependencies
- It is automatically triggered by some commands (e.g. `core add`)

### Typical Use Cases

#### Initial setup

```bash
core sync
```

#### Rebuild environment

```bash
core sync --clean
```

#### Install only runtime dependencies

```bash
core sync --no-dev
```

#### Update a single dependency

```bash
core sync --package requests
```

---


## `core add`

### Overview

Adds a dependency to the project.

This command:

- updates `corellia.toml`
- resolves the package version (if not provided)
- installs the dependency in the environment

### Syntax
```bash
core add <package> [options]
```

### Options

`--version <version>`
Specify the exact version of the package.

```bash
core add requests --version 2.32.3
```

`--dev`
Add the dependency as a development dependency.

```bash
core add pytest --dev
```

### What It Does

The command performs the following steps:

1. resolves the package version (if not provided)
2. updates `corellia.toml`
3. installs the dependency in the virtual environment

Installation is performed using the same logic as:

```bash
core sync --package <package>
```

### Behavior

#### Without version

If no version is specified, Corellia fetches the latest available version and pin it in the `corellia.toml`

#### With version

If a version is provided, it is used directly and no resolution is performed


#### With `--dev`
The package is added to `[dev-dependencies]` otherwise, it is added to `[dependencies]`


### Example

```bash
core add requests
```

```bash
core add pytest --dev
```

```bash
core add fastapi --version 0.115.0
```

### Result

After running the command:

- `corellia.toml` is updated
- the dependency is installed
- the environment is synchronized
  
### Notes
- Versions are always stored explicitly
- The command ensures the environment stays consistent
- No manual editing of dependencies is required

---


## `core remove`

### Overview

Removes a dependency from the project.

This command:

- updates corellia.toml
- removes the dependency from the virtual environment

### Syntax

```bash
core remove <package>
```

### What It Does

The command performs the following steps:

1. removes the package from corellia.toml
2. uninstalls the package from the virtual environment

### Behavior

The package is removed regardless of whether it is a runtime dependency (`[dependencies]`) or a development dependency (`[dev-dependencies]`)

Only the specified package is affected and other dependencies remain unchanged


### Result

After running the command the dependency is removed from configuration and the package is uninstalled from the environment.

### Notes
The command does not reinstall or re-sync other dependencies. If needed, you can run:

```bash
core sync
```

to fully reapply the environment state.


---


## `core run`

### Overview

Executes a project script defined in `corellia.toml`.

This command allows you to run predefined commands within the project's environment, without manually activating the virtual environment.

### Syntax

```bash
core run <script>
```

### Options

`--list`
Lists all available scripts defined in the project.

```bash
core run --list
```

### Scripts Definition

Scripts are defined in `corellia.toml` using the following structure:

```toml
[scripts.<name>]
command = "<command>"
mode = "<mode>"
description = "<optional>"
```

### Execution Modes

`strict`
Runs the command directly.

- executed without a shell
- safer and more predictable
- recommended for most cases


`shell`
Runs the command through a shell.

- allows shell features (pipes, chaining, etc.)
- less strict but more flexible


### What It Does

When executing a script, Corellia:

1. ensures the environment is ready
2. resolves the script definition
3. executes the command using the project’s Python environment

### Example

```bash
core run dev
```

### Listing Scripts

```bash
core run --list
```

Displays all available scripts along with their descriptions.

### Result
The command is executed inside the project’s virtual environment, so no manual activation of `.venv` is required.


### Notes
- Scripts are defined entirely in `corellia.toml`
- The environment is always correctly configured before execution
- Scripts provide a consistent way to run project tasks


---


## `core info`

### Overview

Displays detailed information about the current Corellia project.

This command provides a comprehensive view of:

- project configuration
- Python environment
- virtual environment status
- dependencies
- Git repository status

### Syntax

```bash
core info
```

### What It Does

The command reads the current project configuration and inspects the local environment to produce a structured summary.


### Output Sections

#### Project

Displays core project metadata:

- name
- module (main Python package directory)
- version
- category
- framework
- required Python version

#### Python Environment

Shows the status of the Python setup:

- Python manager (e.g. `pyenv`)
- whether the required Python version is installed
- local Python version binding (`.python-version`)
- consistency between configuration and local setup

#### Virtual Environment

Displays information about the project virtual environment:

- existence of `.venv`
- path to the environment
- readiness status

#### Dependencies

Shows:

- number of runtime dependencies
- number of development dependencies

#### Git

Displays repository status (if Git is available):

- whether the project is a Git repository
- current branch
- remote configuration
- working directory status (clean/dirty)


### Result

The command outputs a structured summary of the project state.

This helps you quickly identify:

- missing environment setup
- mismatched Python versions
- dependency issues
- repository status

### Notes

This command is read-only; it does not modify the project and can be safely executed at any time.


---


## `core init-build`

### Overview

Initializes the packaging configuration for a project.

This command generates the `pyproject.toml` file required to build a distributable Python package.

### Syntax

```bash
core init-build
core init-build --force  # regenerate an existing pyproject.toml
```

### Supported Categories

This command is currently supported only for:

- `package`

### What It Does

The command performs the following steps:

1. validates the project configuration
2. verifies the expected package structure
3. generates a pyproject.toml file

### Requirements

Before running this command:

- The project must have:

    ```toml
    [project]
    category = "package"
    ```

- The package structure must exist:

    ```
    src/<module_name>/__init__.py
    ```

### Generated File

The command creates `pyproject.toml`

This file includes:

- build system configuration (`setuptools`)
- project metadata
- dependencies
- optional development dependencies
- package discovery configuration (`src/` layout)

### Result

After running the command the project is ready for packaging.

### Notes
- The file is generated from `corellia.toml`
- It is considered a **derived artifact**
- It may be regenerated with `core init-build --force` when it already exists
- `--force` overwrites the entire file: manually added settings are not preserved


---


## `core build`

### Overview

Builds a distributable Python package from the current project.

This command produces packaging artifacts such as:

- source distribution (`.tar.gz`)
- wheel (`.whl`)

### Syntax

```bash
core build
```

### Supported Categories

This command is currently supported only for:

- `package`

### Requirements

Before running this command:

- `pyproject.toml` must exist
- `[project].version` in `pyproject.toml` must match `corellia.toml` (use `core init-build --force` to regenerate it if needed)
- the project must have a valid package structure
- the environment must be properly initialized

### What It Does

The command performs the following steps:

1. validates project configuration
2. ensures the environment is ready
3. installs the `build` module (if missing)
4. cleans previous build artifacts
5. executes the build process
6. collects generated artifacts

### Build Process

Corellia executes:

```bash
python -m build
```

using the project's virtual environment.


### Cleaning Strategy

Before building, Corellia cleans previous artifacts:

#### Always removed
- `build/`
- `*.egg-info`

#### Conditionally removed
- files in `dist/` matching the current project version

This ensures:

- clean builds
- no duplicate artifacts for the same version
- preservation of previous versions

### Output

Build artifacts are generated in `dist/`

Example:

```bash
dist/
  myproject-0.1.0.tar.gz
  myproject-0.1.0-py3-none-any.whl
```

### Result

After running the command the project is ready for distribution.

### Notes
- The command uses the project’s Python environment
- No global Python configuration is required
- Build behavior depends on `pyproject.toml`
- The distribution metadata uses `[project].name`; setuptools discovers importable packages under `src/`, including a module with a different name

---

## `core version`

### Overview

Shows or changes the version of the current project. The authoritative version is `[project].version` in `corellia.toml`. This is different from `core --version`, which reports the installed Corellia CLI version.

### Syntax

```bash
core version
core version patch
core version minor
core version major
core version 1.2.3
```

### What It Does

- With no argument, displays the current project version.
- With `patch`, `minor`, or `major`, increments that component and resets lower components as appropriate.
- With `X.Y.Z`, sets an explicit version. The current implementation accepts numeric `MAJOR.MINOR.PATCH` versions.
- Updates `corellia.toml`; for `package` projects, also updates an existing, recognized literal `__version__` assignment in the main package's `__init__.py`.
- Does **not** automatically regenerate `pyproject.toml`.

### Notes

After a package version change, run `core init-build --force` before `core build` if the build metadata is outdated. Regeneration overwrites custom edits to `pyproject.toml`. Git tags, changelogs, prerelease version schemes and publishing are not part of this command.

---

## `core module rename`

### Overview

Renames the main Python module directory and updates `[project].module` in `corellia.toml`. It does **not** change `[project].name`, the distribution name.

### Syntax

```bash
core module rename new_module
```

### What It Does

1. Validates the new module name (lowercase Python identifier, not a keyword).
2. Checks that the original module directory exists and the destination is free.
3. Renames `src/<module>/` for a `package`, or `<module>/` at the project root for `app` and `deploy`.
4. Updates `corellia.toml`; if saving fails, attempts to restore the original directory.

### Constraints

- A project with no explicitly configured module must first be configured manually.
- Django project module renaming is not yet supported.
- Existing Python imports and other module references are **not** rewritten; review them manually after renaming.
- Existing target files or directories are never overwritten.

### Example

For a `package` distribution named `my-project` with a module `my_project`:

```bash
core module rename my_module
core init-build --force
core build
```

The distribution name remains `my-project`, while the wheel includes the importable package `my_module`.
