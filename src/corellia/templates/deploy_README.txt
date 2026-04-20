# <project_name>

Deployable backend project generated with **Corellia**.

## Overview

This project is designed to run as a backend service or server application.

Typical use cases:
- web backend (Django, FastAPI, Flask)
- API services
- background workers
- internal services

---

## Getting Started

### 1. Install dependencies

```bash
core sync
```

### 2. Run the project

Depending on the framework:

#### Django

```bash
core run dev
```

#### Generic Python app

```bash
core run start
```

---

## Project Structure

```bash
.
├── corellia.toml
├── README.md
├── main.py / manage.py
├── app/
│   └── __init__.py
└── config/
```

### Key Concepts
- `main.py` / `manage.py` → entry point
- `mpp/` → business logic
- `monfig/` → configuration files
- `morellia.toml` → project configuration


---

## Development

Add a dependency:

```bash
core add <package>
```

---

Scripts

List scripts:

```bash
core run --list
```

Run script:

```bash
core run <script>
```

---


## Deployment

This project is intended to be deployed on:

- VPS
- cloud platforms
- containers (future support)

### Typical workflow

1. setup environment
2. run application server
3. configure runtime settings

---

Notes

- This project does not use a src layout
- It is optimized for execution and deployment
- Packaging as a Python library is not the primary goal