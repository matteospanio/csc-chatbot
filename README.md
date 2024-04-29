# CSC-chatbot

> A chatbot that tells you about the Centro di Sonologia Computazionale (CSC) of the University of Padova and its people.

## Installation

Requirements:
- Python 3.10 or higher
- [Poetry](https://python-poetry.org/) for managing dependencies or pip
- Makefile to run commands (optional)

To install the project from source you can download the repository:

```bash
git clone https://github.com/matteospanio/csc-chatbot.git
cd csc-chatbot
```

Then you can install the dependencies with Poetry:

```bash
poetry install
```

### Without Poetry (not recommended)

If you don't have Poetry installed, you can install the project with pip by running the following command in the project root directory:

```bash
pip install -e .
```

Otherwise you can install just the dependencies with pip:

```bash
pip install -r requirements.txt
```

## Usage

If you have Poetry installed, you can run the chatbot with the following command:

```bash
poetry run chatbot
```
