# Roadmap

## Overview

Corellia is an evolving project aimed at providing a complete and consistent workflow for Python development.

While the core system is stable, several features are planned to expand its capabilities.

However, Corellia aims to maintain:

- stable CLI commands
- stable configuration format

Breaking changes will be introduced only in major versions.

---

## Current State

Corellia currently provides:

- full project lifecycle management
- environment and dependency orchestration
- script execution
- package build support (`package` category)

---

## Short-Term Goals

### Improve Category Support

- expand `app` category capabilities
- define clear execution model for applications
- introduce build strategies for applications

### Extend Build System

- improve `pyproject.toml` generation
- allow limited customization of build configuration
- refine artifact management

### Improve Developer Experience
- better error messages
- improved CLI feedback
- validation of configuration

---

## Mid-Term Goals

### Application Packaging

Introduce build support for `app` projects:

- standalone executables
- cross-platform builds
- integration with tools like PyInstaller

### Deploy Category Expansion

Define the `deploy` category:

- backend service structure
- framework-first workflows (e.g. Django)
- deployment-ready layouts

### Framework Ecosystem
- add support for additional frameworks
- improve framework bootstrap
- enable deeper integration

---

## Long-Term Goals

### Deployment Workflows

- containerization support (e.g. Docker)
- deployment pipelines
- environment-specific configurations

### Publishing

- support for publishing packages (e.g. PyPI)
- release automation
- versioning workflows

### Advanced Configuration
- optional lockfile support
- extended configuration sections
- plugin or extension system