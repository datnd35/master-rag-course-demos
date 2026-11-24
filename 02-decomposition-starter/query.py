"""Logic RAG. TODO: tự implement theo docs/concepts.md."""

import bs4
from dotenv import load_dotenv
from langchain import hub
from operator import itemgetter
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from colorama import Fore
import warnings


warnings.filterwarnings("ignore")

load_dotenv()


#llm
llm = ChatOpenAI()


#load documents 

loader = WebBaseLoader(
    "https://python.langchain.com/docs/get_started/introduction"
)
docs=loader.load()

loader = WebBaseLoader(
    "https://python.langchain.com/docs/get_started/quickstart"
)

docs.extend(loader.load())


#split documents, create vector store and load embeddings
loader = WebBaseLoader(
    web_paths=("https://python.langchain.com/docs/get_started/introduction",),
    bs_kwargs=dict(
        parse_only=bs4.SoupStrainer(
            class_=("article-header section", "article-header__content", "article-header__footer")
        )
    )
)

#split
text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=500, chunk_overlap=50
)
splits = text_splitter.split_documents(docs)

vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())
retriever = vectorstore.as_retriever()

prompt = PromptTemplate.from_template(
    "Answer the question using only the context below.\n\n"
    "Context:\n{context}\n\nQuestion: {question}\nAnswer:"
)


def query(question: str) -> str:
    context_docs = retriever.invoke(question)
    context = "\n\n".join(d.page_content for d in context_docs)
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"context": context, "question": question})