# Connected Dominating Sets in a Triangulated Graph

An implementation of a greedy algorithm describe in this [research paper](https://arxiv.org/abs/2312.03399) to determine connected dominating sets in a triangulated graph.

## Installation

### Dependencies

- Python 3
- Qhull

### Steps

1. Create a virtual environment
```shell
python3 -m venv venv
```
2. Activate the virtual environment
```shell
source venv/bin/activate
```
3. Install packages
```shell
pip install -r requirements.txt
```

## Usage (Linux or Unix)

1. Activate the virtual environment
```shell
source venv/bin/activate
```

2. Run `cds.py` CLI tool
```shell
python3 src/cds.py <your specific arguments here>
```

> [!WARNING]
> When you're done using the CLI, run in the command prompt `deactivate`

> [!TIP]  
> For formatting and static analysis, run `check.sh`

## Research Paper Credits

Prosenjit Bose, Vida Dujmović, Hussein Houdrouge, Pat Morin, and Saeed Odak. Connected dominating sets in triangulations. arxiv:2312.03399, 2023.
