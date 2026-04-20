# <project_name>

Application project generated with **Corellia**.

## Overview

This project is an executable Python application.

It is designed to be:
- run locally
- developed within the Corellia workflow
- optionally distributed as a standalone application in the future

---

## Getting Started

### 1. Install dependencies

```bash
core sync
```

### 2. Run the application

```bash
core run start
```

Or directly:

```bash
python main.py
```

---

## Project Structure

```
.
├── corellia.toml
├── README.md
├── main.py
├── app/
│   └── __init__.py
└── assets/
```

### Key Concepts
- `main.py` → application entry point
- `app/` → application logic
- `assets/` → static resources (optional)
- `corellia.toml` → project configuration


--- 

## Development

Add a dependency:

```bash
core add <package>
```

---


## Scripts

List available scripts:

```bash
core run --list
```

Run a script:

```bash
core run <script>
```


---

## Notes

- This project does not use a src layout
- It is designed for execution, not packaging
- Corellia manages environment and scripts automatically