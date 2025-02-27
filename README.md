# Chess

## Setup

### Create python virtual environment

```
python3 -m venv .venv
```

### Activate virtual environment

```
source .venv/bin/activate
```

### Deactivate virtual environment

```
deactivate
```

### Install dependencies

With `pyproject.toml`:

```
pip install -e "."
```

(`-e`: install the currently developed package in editable mode)

Previously, using a simple `requirements.txt`:

```
Note: Activate virtual environment first
pip install -r requirements.txt
```
