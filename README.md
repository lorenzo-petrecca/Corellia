# Corellia

Corellia is a CLI framework/toolchain for Python projects, with an initial specialization in Django backend workflows.

## Status

Early development.

## Local development

```bash
pyenv local 3.12.11
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e .[dev]
```

## Run

```bash
core hello
```