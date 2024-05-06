import os

from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.memory import ChatMessageHistory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSerializable
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt

from chatbot.memory import get_memory, load_chat_messages, save_chat_messages


def main_loop(model, embedding, temperature, sys_prompt, api_key):
    console = Console()

    # create models
    llm = ChatOpenAI(
        model=model,
        temperature=temperature,
        api_key=api_key,
    )
    embeddings = OpenAIEmbeddings(
        model=embedding,
        api_key=api_key,
    )
    out_parser = StrOutputParser()

    messages = load_chat_messages()
    history = ChatMessageHistory(messages=messages)

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                sys_prompt,
            ),
            MessagesPlaceholder(variable_name="messages"),
        ],
    )

    retriever = get_memory(embeddings).as_retriever(k=4)
    document_chain = create_stuff_documents_chain(llm, prompt) | out_parser

    console.print("[bold]Session started, press CTRL+C to quit.")
    while True:
        try:
            loop(history, document_chain, retriever, console)
        except KeyboardInterrupt:
            console.print("\n[bold]Shutting down... Goodbye!")
            return exit_handler(history)


def loop(
    history: ChatMessageHistory,
    chain: RunnableSerializable,
    retriever: VectorStoreRetriever,
    console: Console,
) -> None:
    question = Prompt.ask("\n[bold cyan]>>> You")

    history.add_user_message(question)
    with console.status("[bold green]Generating answer..."):
        response = chain.invoke(
            {
                "context": retriever.invoke(question),
                "messages": history.messages,
            },
        )
        history.add_ai_message(response)
        md = Markdown(response)

    console.print(md)


def exit_handler(history: ChatMessageHistory) -> int:
    save_chat_messages(history.messages)
    return os.EX_OK
