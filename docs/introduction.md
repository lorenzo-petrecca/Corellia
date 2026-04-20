# Introduction

## What is Corellia

Corellia is a **command-line tool** designed to **standardize and simplify Python project development**.

It provides a unified workflow to:

- manage Python versions
- create and maintain virtual environments
- install and track dependencies
- structure projects consistently
- execute project scripts
- build distributable Python packages

Corellia acts as an **orchestration layer** on top of existing tools such as `pyenv`, `venv`, `pip`, and `git`, abstracting their complexity into a single, consistent interface.

---

## Why Corellia

Managing a Python project typically involves multiple tools and manual steps:

- selecting a Python version
- creating and activating virtual environments
- installing dependencies
- organizing project structure
- remembering commands and conventions

Corellia solves this by introducing:

- a **single command interface**
- a **single configuration file**
- a **consistent project structure**
- an **opinionated but predictable workflow**

Instead of manually coordinating multiple tools, developers interact only with Corellia.


---

## Design Goals

Corellia is built around a few key principles:

- **Single source of truth**
All project configuration is defined in `corellia.toml`.

- **Deterministic environments**
Dependencies are pinned and environments are reproducible.

- **Minimal abstraction leakage**
Underlying tools are hidden as much as possible.

- **Consistency over flexibility**
Corellia favors a predictable workflow over highly customizable behavior.

- **Incremental extensibility**
The system is designed to grow without breaking existing projects.

---

## Non-goals

Corellia is **not**:

- a replacement for Python itself
- a full deployment platform
- a framework in the traditional sense (like Django or Flask)

It focuses on **project orchestration**, not application logic.