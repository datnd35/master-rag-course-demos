# Starter: nền tảng RAG với ChromaDB

Khung ban đầu: menu CLI, nạp web, chia chunk (300 token, overlap 50), embedding, lưu ChromaDB, tạo retriever.

## Bạn sẽ học
- WebBaseLoader + BeautifulSoup lọc HTML
- RecursiveCharacterTextSplitter
- OpenAIEmbeddings + Chroma
- Tạo retriever
- Dùng .env

## Cấu trúc
- `main.py: menu CLI, vòng lặp hỏi đáp`
- `query.py: load_documents(), split_documents(), create_vectorstore(), get_retriever()`
- `utils.py: hàm in màu, format_qa_pair()`
- `docs/concepts.md`: giải thích khái niệm
- `requirements.txt`, `.env.example`

## Cài đặt & chạy
```
python3 -m venv env && source env/bin/activate
pip install -r requirements.txt
cp .env.example .env   # điền OPENAI_API_KEY
python main.py
```

> Không commit API key thật. Chỉ để trong `.env`.
