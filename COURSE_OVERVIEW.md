# Tổng quan chuỗi project: Advanced RAG với Query Decomposition

Nguồn tham khảo: `course-materials` (starter-project + part 1→4). Các project `02`→`06` là bản làm lại theo từng bước để bạn tự implement.

## Bài toán

RAG thường chỉ tìm kiếm **một lần** cho cả câu hỏi. Với câu hỏi phức tạp (ví dụ: _"What are the main components of an LLM-powered autonomous agent system?"_), một lần tìm thường thiếu thông tin.

**Query Decomposition**: tách câu hỏi lớn thành nhiều câu hỏi nhỏ → mỗi câu hỏi nhỏ retrieve + trả lời riêng → tổng hợp thành câu trả lời cuối.

```
Câu hỏi gốc
   │  (03) LLM sinh 3 sub-questions
   ▼
Sub-question 1..3
   │  (04) trả lời đệ quy: câu sau dùng Q&A của câu trước
   │  (05) hoặc trả lời độc lập (có thể song song)
   ▼
Các cặp Q&A
   │  (06) LLM tổng hợp
   ▼
FINAL ANSWER
```

## Dữ liệu dùng chung

- Hai bài blog LangChain: `https://blog.langchain.dev/deconstructing-rag/` và `https://blog.langchain.dev/reflection-agents/`.
- Vector store: **ChromaDB**; embedding: `OpenAIEmbeddings`; LLM: `ChatOpenAI`.
- Chunk: 300 token, overlap 50 (`RecursiveCharacterTextSplitter.from_tiktoken_encoder`).
- Dùng BeautifulSoup (`bs4.SoupStrainer`) để chỉ lấy phần nội dung bài viết.

## Các project

| #   | Thư mục                                | Là gì                                                                                | Mục đích                                                                      | Bạn học được                                                                                 |
| --- | -------------------------------------- | ------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| 01  | `01-basic-rag`                         | RAG cơ bản: FAISS + `RetrievalQA`                                                    | Hiểu pipeline load → split → embed → store → retrieve → generate              | Nền tảng RAG, lưu/load index FAISS                                                           |
| 02  | `02-decomposition-starter`             | Khung dự án: menu CLI, load dữ liệu, tạo Chroma, retriever. Các hàm chính còn `pass` | Có sẵn hạ tầng để tập trung vào logic decomposition                           | Loader + lọc HTML, splitter theo token, Chroma, `.env`                                       |
| 03  | `03-decomposition-sub-questions`       | Hoàn thiện `generate_sub_questions(query)`                                           | Biến 1 câu hỏi phức tạp thành 3 câu hỏi con                                   | Prompt template, LCEL `prompt \| llm \| parser \| split`, lý do decomposition giúp retrieval |
| 04  | `04-decomposition-answer-recursively`  | Thêm `generate_qa_pairs(sub_questions)`                                              | Trả lời tuần tự, mỗi câu dùng context từ retriever và các Q&A đã có           | `itemgetter` trong chain, kết hợp retrieval + prompt, tích lũy tri thức, `format_qa_pair`    |
| 05  | `05-decomposition-answer-individually` | Thêm `retrieve_and_rag(prompt_rag, sub_questions)`                                   | Trả lời từng câu độc lập bằng prompt RAG chuẩn (`hub.pull("rlm/rag-prompt")`) | So sánh đệ quy vs độc lập, batch/parallel, trade-off tốc độ và độ liên kết                   |
| 06  | `06-decomposition-final-answer`        | Hoàn thiện `query()` và `main.py`                                                    | Ghép toàn bộ pipeline và tổng hợp FINAL ANSWER                                | Ghép nhiều chain, CLI hoàn chỉnh, `colorama`, `format_qa_pairs`                              |

## Chi tiết từng project

### 02 – Starter

- `query.py` ở starter đã có: load 2 blog, lọc HTML, split, tạo `Chroma`, `retriever`, các prompt (decomposition, QA, tổng hợp).
- Các hàm `generate_sub_questions`, `generate_qa_pairs`, `retrieve_and_rag`, `query` còn trống.
- `utils.py` có `format_qa_pair` (in màu từng cặp) và `format_qa_pairs` (gộp text cho bước tổng hợp).

### 03 – Sub-questions

- Prompt yêu cầu LLM "tạo 3 truy vấn con có thể trả lời độc lập".
- Chain: `prompt_decomposition | llm | StrOutputParser() | (lambda x: x.split("\n"))`.
- In kết quả bằng màu `MAGENTA` để dễ theo dõi.

### 04 – Answer recursively

- Với mỗi sub-question: `{"context": itemgetter("sub_question") | retriever, "sub_question": ..., "q_a_pairs": ...} | prompt_qa | llm | StrOutputParser()`.
- Kết quả được nối vào `q_a_pairs` rồi đưa cho câu tiếp theo.
- Ưu: câu sau có ngữ cảnh của câu trước. Nhược: tuần tự, chậm, lỗi lan truyền.

### 05 – Answer individually

- Với mỗi sub-question: `retriever` lấy doc → `prompt_rag | llm | StrOutputParser()`.
- Trả về `(answers, questions)` để dùng cho bước tổng hợp.
- Ưu: độc lập, dễ song song. Nhược: không tận dụng Q&A trước.

### 06 – Final answer

- `query()`: sinh sub-questions → `retrieve_and_rag` → `format_qa_pairs(questions, answers)` → chain `prompt | llm | StrOutputParser()` với `{"context": ..., "question": ...}`.
- `main.py`: menu, vòng lặp nhập câu hỏi, in "FINAL ANSWER".

## Lưu ý

- Mã tham khảo dùng `retriever.get_relevant_documents(...)`; ở phiên bản LangChain mới hơn nên dùng `retriever.invoke(...)`.
- Trong code tham khảo, hàm `query()` ở part 2/3 còn dùng danh sách câu hỏi cố định để thử nghiệm; bản hoàn chỉnh dùng câu hỏi người dùng nhập.
- Không commit API key; chỉ đặt trong `.env`.
