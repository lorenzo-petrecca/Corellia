# Getting Started

## Prerequisites

Before using Corellia, make sure the following tools are installed on your system:

- **Python** (recommended: 3.10+)
- **pyenv** (for Python version management)
- **git** (optional, but recommended)

Corellia relies on these tools internally to manage environments and project setup.

---

## Installation

Corellia can be installed globally using `pipx` (recommended) or `pip`.

**Using pipx**

```bash
pipx install corellia
```

**Using pip**

```bash
pip install corellia
```

Once installed, the **`core`** command will be available globally.

---

## Create a New Project

To create a new project, run:

```bash
core create
```

Corellia will guide you through an interactive setup:

- project name
- Python version
- category (`package`, `app`, `deploy`)
- optional framework (e.g. `django`)

After confirmation, Corellia will:

1. create the project directory
2. generate corellia.toml
3. set the Python version via pyenv
4. create a virtual environment (.venv)
5. install dependencies
6. scaffold the project based on category
7. optionally initialize a Git repository


## Install and Sync Dependencies

To install or update dependencies defined in `corellia.toml`, run:

```bash
core sync
```

This will:

- ensure the correct Python version is active
- prepare the virtual environment
- install all runtime and development dependencies

---

## Run Project Scripts

Corellia allows you to define scripts in `corellia.toml`.

To execute a script:

```bash
core run <script>
```

Example:

```bash
core run dev
```

To list available scripts:

```bash
core run --list
```

All scripts are executed **inside the project’s virtual environment**.

---

## Inspect Project Information

To view detailed information about the current project:

```bash
core info
```

This includes:

- project metadata
- Python environment status
- virtual environment details
- dependencies
- Git status

---

## Typical Workflow

A typical development flow with Corellia looks like this:

```bash
core create
cd <project>

core sync
core run <script>
```

For package projects:

```bash
core init-build
core build
```

<!-- ---
## Next Steps
- Learn how the project is configured in Project Configuration
- Understand the underlying model in Core Concepts
- Explore all available commands in Commands -->