# RAG Indexing Flow

## Tổng quan

```
Original Document
       |
       v
Text Splitter
       |
       v
  37 Chunks
       |
       v
OpenAI Embeddings
       |
       v
  37 Vectors
       |
       v
  FAISS Index
       |
       +-------------------+
       |                   |
       v                   v
  index.faiss          index.pkl
  Vector Index         Document Store
                           |
                           v
                       Metadata
                           |
                           v
                       index.json
                       (bản export)
```

## Các bước

### 1. Documents

Dữ liệu lấy từ LangChain Documentation (`WebBaseLoader`).

### 2. Text Splitter

`RecursiveCharacterTextSplitter` (chunk_size=1000, chunk_overlap=200) chia document thành 37 chunks.

### 3. OpenAI Embeddings

Gửi chunks lên OpenAI API để chuyển thành 37 vectors.

### 4. FAISS Vector Store

Lưu vector index và document metadata trong RAM.

### 5. Lưu ra đĩa (`save_local`)

- `index.faiss`: vector index (các vector).
- `index.pkl`: docstore (nội dung chunk + metadata) và mapping index -> doc id.
- `index.json`: file export metadata để dễ đọc (do code tự tạo, không dùng để load lại).

### 6. Python process kết thúc

Dữ liệu FAISS trong RAM bị giải phóng. Các file trong `faiss_index/` còn lại trên đĩa, có thể load lại bằng `FAISS.load_local(...)` mà không cần embed lại (tiết kiệm chi phí API).

## Luồng truy vấn (Query)

```
User Query -> Embedding -> FAISS similarity search (k=3)
           -> Retrieved chunks -> Prompt (question + context)
           -> LLM (gpt-4o-mini) -> Answer
```
