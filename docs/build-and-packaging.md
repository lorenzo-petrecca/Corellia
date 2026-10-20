# Build & Packaging

## Overview

Corellia provides a structured workflow for building distributable Python packages.

This workflow separates:

- **project configuration** → corellia.toml (including distinct distribution name and module name)
- **build configuration** → pyproject.toml
- **build artifacts** → files in dist/

This separation ensures:

- clarity
- reproducibility
- compatibility with the Python packaging ecosystem

---


## Packaging Model

Corellia follows a **two-step packaging model**:

1. generate build configuration
2. execute the build

### Step 1 — Initialize build configuration

```bash
core init-build
```

Generates `pyproject.toml`; use `core init-build --force` to overwrite an existing file. Existing manual customizations are not preserved.

### Step 2 — Build the package

```bash
core build
```

Produces `dist/`

---

## Generated `pyproject.toml`

The `pyproject.toml` file is generated automatically from `corellia.toml`.

It contains:

- build system configuration (setuptools)
- project metadata
- dependencies
- development dependencies
- package discovery configuration

### Example (simplified)

```bash
[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "my-project"
version = "0.1.0"
dependencies = [
  "requests==2.32.3"
]

[project.optional-dependencies]
dev = [
  "pytest==8.3.0"
]

[tool.setuptools]
package-dir = {"" = "src"}

[tool.setuptools.packages.find]
where = ["src"]
```

---

The `[project].name` value is the **distribution name**, not necessarily the importable package. For example, `corellia.toml` may declare `name = "my-project"` and `module = "my_module"`: the generated wheel includes `my_module/`, while the distribution metadata identifies `my-project`. Setuptools discovers Python packages under `src/`.

`core build` checks that the version declared in `pyproject.toml` matches `[project].version` in `corellia.toml`. A mismatch prevents a build until metadata is regenerated.

---

## Build Lifecycle

The full packaging lifecycle is:

```bash
core create
core sync
core init-build
core build
```

### Lifecycle Breakdown

1. **Project setup**
    Corellia initializes environment and structure
2. **Dependency synchronization**
    All dependencies are installed
3. **Build configuration generation**
    pyproject.toml is created (or deliberately regenerated with `--force`)
4. **Build execution**
    Package artifacts are generated

---

## Build Artifacts

After running core build, artifacts are created in `dist/`

### Types of artifacts

#### Source distribution (sdist)

`myproject-0.1.0.tar.gz`

Contains:

- source code
- metadata

#### Wheel

`myproject-0.1.0-py3-none-any.whl`

Contains:

- pre-built package
- ready for installation

---

## Cleanup Strategy

Before building, Corellia cleans up previous artifacts to ensure:

- clean builds
- no duplicate artifacts
- preservation of previous versions

The following are always removed after each build:
- build/
- *.egg-info

These are temporary build artifacts that can be safely removed.

Additionally, existing files in `dist/` are replaced if the current version matches a previous build.

---

## Environment Usage

The build process uses:

- the project’s Python version
- the project’s virtual environment

Corellia runs:

```bash
python -m build
```

using the environment managed by the project.

---

## Supported Categories

Build and packaging are currently supported only for:

- `package`

---

## Limitations

Current limitations include:

- no build support for `app`
- no build support for `deploy`
- no automated publishing (e.g. PyPI)
- limited customization of `pyproject.toml`; regeneration currently replaces the entire file

---

## Design Rationale

Corellia intentionally separates:

- project definition (`corellia.toml`)
- build system (`pyproject.toml`)

This provides:

- compatibility with standard Python tooling
- a clean abstraction layer
- the ability to evolve build strategies independently

---

## Future Extensions

Planned improvements may include:

- build support for `app` (e.g. standalone executables)
- deployment artifacts for `deploy`
- publishing workflows
- extended build configuration with preservation of user-managed fields

---

## Best practice

- **Regenerate build configuration when needed**
    `core init-build` (or `core init-build --force` to regenerate)
- **Build after updating version**
    First synchronize build metadata when necessary, then run `core build`
- **Avoid modifying build artifacts**
    Artifacts in `dist/` should not be manually edited.