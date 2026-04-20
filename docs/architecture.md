# Architecture

## Overview

**Corellia** is built as a **layered orchestration system** that coordinates multiple responsibilities involved in Python project development.

Instead of directly exposing low-level tools such as pyenv, venv, or pip, Corellia:

- abstracts them into dedicated components
- organizes them into logical layers
- orchestrates them through a central manager

---

## Design Philosophy

Corellia’s architecture is guided by the following principles:

### Separation of concerns

Each component is responsible for a single aspect of the system:

- environment management
- dependency management
- project orchestration

### Layered abstraction

Higher-level components orchestrate lower-level ones without exposing internal complexity.

### Explicit orchestration

Every operation follows a clear and traceable sequence of steps.
There is no hidden or implicit behavior.

---

## System Overview

The system can be visualized as a set of coordinated components grouped by responsibility:

```mermaid
graph TD

CLI --> PM[Project Manager]

PM --> GIT[Git Integration]
PM --> ENV[Environment Layer]
PM --> SRV[Service Layer]


ENV --> PY[Python Environment Manager]
ENV --> VENV[Virtual Environment Manager]
ENV --> PKG[Package Manager]
ENV --> RES[Package Resolver]

SRV --> CAT[Category Service]
SRV --> SCAF[Scaffold Service]

SRV --> FW[Framework Integration]

```

### Interpretation
- **CLI Layer**
  Entry point for all user interactions.
- **Project Manager**
  Central orchestrator that coordinates all operations.
- **Environment Layer**
  Handles Python versions, virtual environments, and dependencies.
- **Service Layer**
  Handles scaffolding, category logic, and framework integration.
- **Git Integration**
  Optional layer for repository management.


---


## Core Components


### Project Manager

The `ProjectManager `is the central component of Corellia.

**Responsibilities**:

- load and validate corellia.toml
- coordinate all operations
- implement command logic
- orchestrate managers and services

All CLI commands delegate execution to this component.


### Python Environment Manager

Handles Python version management:

- interacts with `pyenv`
- ensures required Python version is installed
- sets local Python version


### Virtual Environment Manager

Handles the project virtual environment:

- creates `.venv`
- ensures environment exists
- provides Python executable path
- executes commands inside the environment


### Package Manager

Handles dependency installation:

- installs packages via `pip`
- uninstalls packages
- upgrades `pip`


### Category Service

Handles:

- project structure generation
- category-specific logic
- build file generation (pyproject.toml)
- build artifact cleanup


### Scaffold Service

Provides utilities for:

- creating directories
- writing files
- generating templates


### Framework Integration

Handles framework-specific logic:

- framework bootstrap (e.g. Django)
- predefined scripts
- framework extensions


### Git Integration

Provides optional Git support:

- repository initialization
- repository inspection
- status reporting


---


## Execution Flows

Corellia operations follow explicit and deterministic flows.


### `core create`

```mermaid
graph TD
A[CLI: core create] --> B[Collect user input]
B --> C[Create project directory]
C --> D[Resolve framework dependencies]
D --> E[Generate corellia.toml]
E --> F[Set local Python version]
F --> G[Create virtual environment]
G --> H[Upgrade pip]
H --> I[Install dependencies]
I --> J[Install dev dependencies]
J --> K[Bootstrap framework]
K --> L[Apply category scaffolding]
L --> M[Create .gitignore]
M --> N[Initialize Git repository]
```


### `core sync`

```mermaid
graph TD
    A[CLI: core sync] --> B[Load project configuration]
    B --> C[Ensure Python version]
    C --> D[Ensure virtual environment]

    D --> E{Clean rebuild?}
    E -- Yes --> F[Recreate virtual environment]
    E -- No --> G[Keep existing environment]

    F --> H[Upgrade pip]
    G --> H[Upgrade pip]

    H --> I{Single package?}
    I -- Yes --> J[Install selected package]
    I -- No --> K[Install runtime dependencies]

    K --> L{Install dev dependencies?}
    L -- Yes --> M[Install dev dependencies]
    L -- No --> N[Finish]

    J --> N
    M --> N
```


### `core build`

```mermaid
graph TD
    A[CLI: core build] --> B[Load project configuration]
    B --> C[Validate category = package]
    C --> D[Check pyproject.toml]
    D --> E[Validate package layout]
    E --> F[Ensure environment ready]
    F --> G[Clean build artifacts]
    G --> H[Install build module]
    H --> I[Run python -m build]
    I --> J[Collect artifacts from dist]
```


### Data Flow

Corellia is driven by a clear data flow model:

```mermaid
graph LR
    CONFIG[corellia.toml] --> PM[Project Manager]

    PM --> ENV[Environment setup]
    PM --> DEPS[Dependency installation]
    PM --> BUILD[Build configuration]

    BUILD --> PYPROJECT[pyproject.toml]
    BUILD --> DIST[dist/]
```


---


## Configuration-Driven Design

All behavior in Corellia originates from `corellia.toml`.

This file controls:

- environment setup
- dependencies
- scripts
- project structure
- build configuration

All other artifacts are derived from it.

---


## Managers vs Services

Corellia distinguishes between two types of components.

### Managers

Managers are:

- state-aware
- long-lived
- responsible for core system operations

Examples:

- ProjectManager
- PythonEnvManager
- VirtualEnvManager
- PackageManager


### Services

Services are:

- stateless or short-lived
- task-oriented
- used during specific operations

Examples:

- CategoryService
- ScaffoldService
- DjangoService


---


## Summary

Corellia is built as:

- a layered system
- with a central orchestrator
- composed of managers and services
- driven entirely by configuration

This architecture allows Corellia to remain simple for users and scalable over time