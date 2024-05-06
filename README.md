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

## Configuration

Configuration is done through the `config.yml` to set the models parameters. In addition you need to set some environment variables:

- OPENAI_API_KEY to use the OpenAI API
- PDF_PATH, the path to the PDF files to load
- DATA_PATH, the path to the web links to load
- CHROMA_PATH the folder name where to store the chroma database files
- CHAT_MEMORY the file name where to store the chat messages history

## Usage

### with poetry
If you have Poetry installed, you can run the chatbot with the following command:

```bash
poetry run chatbot --help
```

or enter the virtual environment with:

```bash
poetry shell
```

and then run the chatbot with:

```bash
chatbot --help
```

### without poetry
If you installed the project with pip, you can run the chatbot with:

```bash
chatbot --help
```

If you installed only the dependencies with pip, you can run the chatbot with:

```bash
python src/chatbot/ --help
```

## Features/Commands

The CLI chatbot has the following commands:

- `--help`: show the help message
- `--version`: show the version of the chatbot
- `chat`: start the chatbot
- `ingest`: setup the chatbot

`chat` starts the chatbot and you can ask questions about the CSC and its people.

`setup` is used to setup the chatbot memory. It will read the data from the `data` directory and store it in the chatbot memory. It accepts two flags:

- `--with-pdf`: Load the PDF files in the `data/pdf` directory, extract the text and store it in the chatbot memory
- `--with-web`: Load the web pages in the `data/csc.yml` file, extract the text and store it in the chatbot memory

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
