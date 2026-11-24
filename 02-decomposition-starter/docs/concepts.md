# Khái niệm: Starter

## Là gì
Khung dự án: nạp dữ liệu, tạo vector store, retriever, các prompt. Các hàm logic chính còn trống để bạn điền ở các project sau.

## Mục đích
Chuẩn bị hạ tầng RAG để tập trung vào decomposition.

## Dữ liệu
2 blog LangChain: deconstructing-rag, reflection-agents.

## Luồng
WebBaseLoader (+ bs4.SoupStrainer) -> RecursiveCharacterTextSplitter.from_tiktoken_encoder(300, 50) -> Chroma.from_documents(OpenAIEmbeddings) -> as_retriever()

## Bạn học được
- Load web và lọc HTML
- Chia chunk theo token
- Embedding + Chroma
- Retriever, `.env`
- `format_qa_pair`, `format_qa_pairs` trong utils.py

## Việc cần làm
- [ ] Tự implement theo luồng trên
