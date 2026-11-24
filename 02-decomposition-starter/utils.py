"""Hàm hỗ trợ dùng chung cho ingest.py và query.py."""

import hashlib

from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

PERSIST_DIR = "./chroma_db"
COLLECTION_NAME = "vnexpress"
URLS = [
    "https://vnexpress.net/thong-diep-5-tu-cua-elon-musk-khi-jensen-huang-phuc-chuc-5148278.html",
    "https://vnexpress.net/intel-sa-thai-mot-phan-nhan-su-it-toan-cau-5147238.html",
]


def make_id(doc) -> str:
    """ID xác định (deterministic) theo source + nội dung chunk."""
    key = f"{doc.metadata.get('source', '')}::{doc.page_content}"
    return hashlib.sha256(key.encode("utf-8")).hexdigest()


def get_vectorstore() -> Chroma:
    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=OpenAIEmbeddings(),
        persist_directory=PERSIST_DIR,
    )
