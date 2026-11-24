"""Ingest idempotent: chạy nhiều lần vẫn không tạo bản ghi trùng."""

import warnings

from dotenv import load_dotenv
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from utils import URLS, get_vectorstore, make_id

warnings.filterwarnings("ignore")
load_dotenv()


def ingest() -> None:
    docs = []
    for url in URLS:
        docs.extend(WebBaseLoader(url).load())

    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=500, chunk_overlap=50
    )
    splits = splitter.split_documents(docs)
    for i, d in enumerate(splits):
        d.metadata["chunk_index"] = i

    # Loại trùng trong cùng batch
    unique = {}
    for d in splits:
        unique.setdefault(make_id(d), d)

    vectorstore = get_vectorstore()
    existing = set(vectorstore.get(ids=list(unique))["ids"])
    new_ids = [i for i in unique if i not in existing]

    if new_ids:
        vectorstore.add_documents([unique[i] for i in new_ids], ids=new_ids)

    print(f"Chunks: {len(splits)} | unique: {len(unique)} | new: {len(new_ids)}")
    print(f"Tổng bản ghi trong Chroma: {vectorstore._collection.count()}")


if __name__ == "__main__":
    ingest()
