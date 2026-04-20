# CLI Design Principles

## Overview

Corellia is designed as an **opinionated CLI tool**.
Rather than exposing raw flexibility, it provides a structured and consistent workflow for managing Python projects.
These principles guide all design decisions in Corellia.

---

## Single source of true

Corellia uses a single configuration file: `corellia.toml`
This file defines:

- project configuration
- dependencies
- scripts
- environment

All commands operate based on this file.

Corellia is fully driven by configuration. Commands do not introduce implicit state; instead, they read the configuration and apply the desired state, thereby ensuring predictability and reproducibility.

---

## Deterministic Environments

Corellia requires the use of explicit dependency versions to ensure consistent environments and reproducible configurations, and to prevent unexpected updates.
For example:

```toml
requests = “2.32.3”
```

---

## Orchestration

Corellia does not replace existing tools, but coordinates them. This allows Corellia to remain lightweight and compatible with standard tools, and enables each project to leverage established ecosystems.

- `pyenv` → Python version management
- `venv` → virtual environments
- `pip` → dependency installation

---

## Opinionated structure

Corellia enforces a structured approach:

- defined project categories
- standardized configuration
- consistent workflows

This reduces decision fatigue and inconsistent project setups.

---

## Immediate Feedback

These commands apply changes immediately to keep the configuration up to date and prevent any discrepancies between the configuration and the environment.

Examples:

- `core add` → updates config and installs dependency
- `core remove` → updates config and uninstalls dependency

---

## Minimal Abstraction Leakage

Corellia hides low-level complexity when possible.

Users interact with:

- a single CLI
- a single configuration file

Instead of managing multiple tools directly.

---

## Summary

Corellia’s CLI is designed to be:

- predictable
- consistent
- configuration-driven
- explicitly controlled

These principles ensure a smooth and scalable development experience.