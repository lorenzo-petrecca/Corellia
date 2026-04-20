# <project_name>

Python package generated with **Corellia**.

## Overview

This project is structured as a reusable Python package.

It can be:
- imported in other Python projects
- installed via `pip`
- optionally published to PyPI

---

## Getting Started

### Install dependencies and sync project

```bash
core sync
```

---

## Project Structure

```
.
├── corellia.toml
├── README.md
├── src/
│   └── <project_name>/
│       └── __init__.py
└── tests/
    └── __init__.py
```


---


## Development

Add a dependency:

```bash
core add <package>
```

Add a dev dependency:

```bash
core add <package> --dev
```

---


## Build

Initialize build configuration:

```bash
core init-build
```

Build the package:

```bash
core build
```

Artifacts will be generated in:

```bash
dist/
````

---

## Distribution

You can distribute this package via:

- PyPI
- private package registry
- local wheel installation

---

## Notes
- The project uses a **src layout**
- Dependencies are managed declaratively via `corellia.toml`
- Build configuration is generated automatically