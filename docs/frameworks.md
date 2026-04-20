# Frameworks

## Overview

Frameworks in Corellia provide **optional functionality layers** that extend a project.

They are used to:

- bootstrap project-specific structures
- install predefined dependencies
- provide ready-to-use scripts
- enable framework-specific workflows

Frameworks are defined in `corellia.toml`:

```toml
[framework]
name = "django"
```

---

## Framework Model

A framework in Corellia is:

- optional
- applied at project creation
- independent from category

This means:

- a project can exist without a framework
- a framework does not define the project type
- frameworks extend, but do not replace, categories

---

## Supported Frameworks

Currently supported:

- `none`
- `django`

### `none`

#### Purpose

Represents a project without any framework.

#### Behavior

- no additional dependencies
- no additional files
- no predefined scripts

This is the default option.

<br/>

### `django`

#### Purpose

Adds support for building a Django-based project.

When `django` is selected, Corellia:

- installs Django as a dependency
- generates a Django project
- integrates it into the Corellia structure
- provides default scripts
  
#### Example Scripts

Corellia may automatically define scripts such as:

```toml
[scripts.runserver]
command = "python manage.py runserver"
mode = "shell"

[scripts.migrate]
command = "python manage.py migrate"
mode = "strict"
```

#### Project Integration

Django is integrated as part of the project structure, not as a separate system.

Corellia:

- prepares the environment
- installs dependencies
- delegates application logic to Django

---

## Framework Lifecycle

Frameworks are primarily applied during:

```bash
core create
```

After creation:

Corellia does not dynamically “switch” frameworks
changes must be handled manually or via future tooling

---

## Framework vs Category

This is a key concept.

**Category** defines:

- what the project is
- its structure
- its build model

**Framework** defines:

- what the project uses
- additional capabilities
- specific workflows

Example

```toml
[project]
category = "deploy"

[framework]
name = "django"
```

- `category = deploy` → backend/service project
- `framework = django` → implemented using Django

---

## Design Philosophy

Corellia treats frameworks as **extensions**, not foundations and as **replaceable layers**, not core constraints.

This allows:

- flexibility across project types
- consistent Corellia workflow
- separation between structure and implementation

---

## Limitations

Current limitations:

- only basic framework support
- limited automation after project creation
- no framework switching

Future versions may include:

- more frameworks
- deeper integration
- framework-specific tooling
