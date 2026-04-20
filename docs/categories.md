# Categories

## Overview

Every Corellia project belongs to a **category**.

The category defines:

- the project structure  
- the intended usage  
- the available capabilities  
- the supported build workflows  

Categories are defined in `corellia.toml`:

```toml
[project]
category = "package"
```

---

## Available Categories

Corellia currently supports three categories:

- `package`
- `app`
- `deploy`

Each category represents a different type of project. 

### `package`

#### Purpose

A package project is a **reusable Python library**.

It is designed to:

- be imported by other Python projects
- be installed via pip
- be distributed (e.g. via PyPI)

#### Structure

```
project/
  src/
    <project_name>/
      __init__.py
  tests/
```

#### Characteristics

- uses `src/` layout
- supports packaging and distribution
- supports `core init-build` and `core build`
- produces artifacts in `dist/`


#### Build Support
Fully supported.

```bash
core init-build
core build
```

<br/>

### `app`

#### Purpose

An app project is an **executable Python application**.

It is designed to:

- run locally
- provide a user-facing or internal tool
- be executed via scripts or entrypoints

#### Structure

```
project/
  main.py
  app/
    __init__.py
```

#### Characteristics

- entrypoint-based execution (`main.py`)
- does not use `src/` layout
- focuses on runtime behavior rather than distribution

#### Build Support

Currently not supported.
Future versions may introduce:

- standalone executables
- application packaging

<br/>

### `deploy`

#### Purpose

A deploy project is intended for deployment environments.

Examples include:

- backend services
- APIs
- long-running processes

#### Structure

Currently minimal and subject to future evolution.

May include:

- framework-specific layouts (e.g. Django)
- service-oriented structure
- configuration layers

#### Characteristics

- designed for server/runtime environments
- may integrate with frameworks
- focuses on execution and deployment

#### Build Support

Not supported yet.
Future support may include:

- containerization (e.g. Docker)
- deployment artifacts

---

## Category-Based Scaffolding

When creating a project, Corellia generates a base structure depending on the selected category.

This includes:

- directories
- initial files
- project layout

The scaffolding is handled automatically during:

```bash
core create
```

---

## Category vs Framework

Categories and frameworks are independent concepts.

- **Category** defines the project type
- **Framework** defines additional capabilities

Example:

- `category = "deploy"`
- `framework = "django"`

In this case:

- the category defines the general structure
- the framework adds specific functionality

---

## Choosing the Right Category

Choose a category based on the **primary purpose** of your project:

- use `package` if you want to distribute a library
- use `app` if you want to build an executable tool
- use `deploy` if you are building a backend or service