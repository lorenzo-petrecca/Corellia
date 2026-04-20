# Core Concepts

## Projects

A Corellia project is a directory managed through the CLI and defined by a `corellia.toml` file.

It includes:

- configuration
- environment setup
- dependencies
- scripts
- optional framework integration

---

## Source of Truth

The `corellia.toml` file is the central configuration of a project.

It defines:

- project metadata
- Python version
- category
- dependencies
- scripts

All operations performed by Corellia derive from this file.

---

## Environment Management

Corellia manages the project environment automatically.

## Python version

Each project is tied to a specific Python version (via `pyenv`).

## Virtual environment

Each project has its own isolated virtual environment (`.venv`).

Corellia ensures that:

- the correct Python version is used
- the virtual environment is created and reused
- commands run inside the correct environment

---

## Categories

Each project belongs to a **category**, which defines its structure and capabilities.

### `package`

- reusable Python library
- uses src/ layout
- supports packaging and distribution

### `app`

- executable Python application
- structured around an entrypoint (main.py)
- designed for local execution

### `deploy`

- project intended for server or deployment environments
- currently minimal, designed for future expansion


Categories influence:

- project scaffolding
- supported commands
- build behavior

---

## Frameworks

A framework is an **optional layer** that extends a project with specific capabilities.

Examples:

- `django`
- `none`

Frameworks are applied during project creation and may:

- generate additional files
- add dependencies
- define default scripts

Frameworks are **independent from categories**.

---

## Dependencies

Corellia distinguishes between two types of dependencies:

- **Runtime dependencies**
    Required for the project to run.

- **Development dependencies**
    Used for development only (testing, linting, etc.).

All dependencies are defined in `corellia.toml` and installed via `core sync`.

---

## Scripts

Scripts define executable commands within the project.

Each script includes:

- `command`: the command to run
- `mode`: execution mode (`strict` or `shell`)
- `description`: optional description

---

## Derived Artifacts

Corellia generates several artifacts from the project configuration:

- `.venv/` → virtual environment
- `.python-version` → Python version binding
- `pyproject.toml` → packaging configuration (for package)
- `dist/` → build output

These artifacts are **derived**, not manually edited.