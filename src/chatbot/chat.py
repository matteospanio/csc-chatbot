import os
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSerializable
from langchain_core.vectorstores import VectorStoreRetriever
from langchain.memory import ChatMessageHistory
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt

from chatbot.memory import get_memory, load_chat_messages, save_chat_messages

SYS_PROMPT = """You are a very patient and funny helper, you attend the Center for Computational Sonology at the University of Padua and you know all the other people who work there. \
Your task is to provide information about the Computational Sonology Center, the people who are part of it and the plans for carrying out a thesis at the Center, don't answer questions about other topics. \
You always start an answer by telling a joke about the Center or the people who work there.
Answer the user's questions based on the below context.
If the context does not contain information to answer the user's question, ask the user to provide more information in a funny way.

<context>
{context}
</context>
"""


def main_loop():
    console = Console()

    # create models
    llm = ChatOpenAI(model="gpt-4-turbo", temperature=0.7)
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    out_parser = StrOutputParser()

    messages = load_chat_messages()
    history = ChatMessageHistory(messages=messages)

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                SYS_PROMPT,
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )

    retriever = get_memory(embeddings).as_retriever(k=4)
    document_chain = create_stuff_documents_chain(llm, prompt) | out_parser

    # chain = (
    #     RunnablePassthrough.assign(context=parse_retriever_input | retriever).assign(
    #         answer=document_chain
    #     )
    #     | out_parser
    # )

    console.print("[bold]Session started, press CTRL+C to quit.")
    while True:
        try:
            loop(history, document_chain, retriever, console)
        except KeyboardInterrupt:
            console.print("\n[bold]Shutting down... Goodbye!")
            return exit_handler(history)


def parse_retriever_input(params):
    return params["messages"][-1].content


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
            }
        )
        history.add_ai_message(response)
        md = Markdown(response)

    console.print(md)


def exit_handler(history: ChatMessageHistory) -> int:
    save_chat_messages(history.messages)
    return os.EX_OK
