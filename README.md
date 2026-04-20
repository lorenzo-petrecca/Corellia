![Status](https://img.shields.io/badge/status-experimental-orange)
![License](https://img.shields.io/badge/license-MIT-green)

# Corellia

Corellia is an opinionated CLI tool for managing Python projects.

It provides a unified workflow to:

* manage Python versions
* create and manage virtual environments
* install and track dependencies
* structure projects consistently
* execute project scripts
* build distributable packages

---

## Why Corellia

Python development often requires coordinating multiple tools:

* pyenv
* venv
* pip
* git

Corellia orchestrates them into a **single, consistent interface**, reducing setup complexity and improving reproducibility.

---

## Installation

```bash
pipx install corellia-cli
```

> [!WARNING]
> Corellia is currently in early release.

### Prerequisites
- Python 3.12+
- pyenv
- Git (recommended)


### Frome source

```bash
git clone https://github.com/lorenzo-petrecca/Corellia.git
cd corellia
pipx install -e .
```

---

## Quick Start

### Create a project

```bash
core create
```

### Install dependencies

```bash
core sync
```

### Run scripts

```bash
core run <script>
```

### Build a package

```bash
core init-build
core build
```

---

## Core Concepts

* **Single source of truth** → `corellia.toml`
* **Deterministic environments** → pinned dependencies
* **Categories** → `package`, `app`, `deploy`
* **Frameworks** → optional extensions (e.g. Django)

---

## Example Project

```toml
[project]
name = "myproject"
version = "0.1.0"
python = "3.12"
category = "package"

[dependencies]
requests = "2.32.3"

[scripts.dev]
command = "python main.py"
mode = "strict"
```

---

## Documentation

Full documentation is available in the `/docs` directory.

---

## Roadmap

* app build support
* deploy workflows
* additional frameworks
* packaging improvements

---

## License

This project is licensed under the MIT License.

