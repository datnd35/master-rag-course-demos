# Câu hỏi ôn tập: Starter (RAG + Decomposition)

## Phần 1: Khái niệm cơ bản

1. Mục đích của project "Starter" là gì? Vì sao cần chuẩn bị hạ tầng RAG trước khi học decomposition?
2. RAG là gì? Nêu 3 bước chính trong một pipeline RAG.
3. Decomposition (phân rã câu hỏi) giải quyết vấn đề gì của RAG thông thường?

Trả lời:

- Mục đích của project "Starter" là xây dựng hệ thông RAG cơ bản, chuẩn bị hạ tầng để học decomposition. Vì nếu ko có hạ tầng RAG thì việc học decomposition sẽ khó khăn hơn, vì ko có dữ liệu và hạ tầng để thực hành.

- RAG (retrieval - augmented generation) là architecture kết hợp retrieval và generation. có 3 bước chính:

1. Nap dữ liệu (load data)
2. Chia chunk
3. Embedding & Vector store

- Decomposition giúp chia câu hỏi phức tạp thành các câu hỏi con, giúp retriever tìm tài liệu liên quan dễ dành hơn, tránh thất bại khi câu hỏi có nhiều ý.

## Phần 2: Nạp dữ liệu

4. `WebBaseLoader` dùng để làm gì?
5. `bs4.SoupStrainer` có vai trò gì? Vì sao nên lọc HTML trước khi chia chunk?
6. Dữ liệu trong project gồm những nguồn nào? (deconstructing-rag, reflection-agents)

- WebBaseLoader: Là một class trong langchain dùng để truy xuất nội dung từ web, giúp loại các phần ko cần thiết như quảng cáo, menu, footer,...để chỉ lấy nội dung chính của trang web như nội dung.

- bs4.SoupStrainer là một class trong thư viện BeatifulSoup giúp lọc các phần từ html theo điều kiện nhất định.

- Dữ liệu trong project gồm các nguồn: deconstructing-rag, reflection-agents.

## Phần 3: Chia chunk

7. Vì sao cần chia tài liệu thành các chunk nhỏ?
8. `RecursiveCharacterTextSplitter.from_tiktoken_encoder(300, 50)`: `300` và `50` nghĩa là gì?
9. Chunk overlap giúp ích gì? Điều gì xảy ra nếu overlap = 0?
10. Chia theo token khác chia theo ký tự như thế nào?
11. Chunk quá nhỏ hoặc quá lớn ảnh hưởng gì đến chất lượng truy xuất?

- Chia chunk giúp độ dài tài liệu tránh vượt quá giới hạn token của llm đồng thời cũng giúp retrvier tìm tài liệu liên quan dễ dàng hơn, vì retriver dự vào độ tương đồng của vertor câu hỏi và chunk.

- RecursiveCharacterTextSplitter.from_tiktoken_encoder(300, 50): `300` là kích thước chunk của token, 50 là số token chồng lấn giữa các chunk.

- Chunk overlap dùng để giảm ngữ cảnh ranh giới giữa các chunk.

- chia theo token giúp giữ nguyên ý của câu trong khi đó chia theo kí tự có thể làm mất ý nghĩa cua câu.

- Chunk quá nhỏ hooặc quá lớn ảnh hưởng đến chất lượng của việc truy suất, chunk quá nhỏ có thể làm mất ngữ cảnh trong khi đó chunk quá lớn có thể vượt quá token giới hạn của llm.

## Phần 4: Embedding & Vector store

12. Embedding là gì? `OpenAIEmbeddings` được dùng để làm gì?
13. `Chroma.from_documents` thực hiện những việc gì?
14. Thư mục `chroma_db/` lưu gì? Khi chạy lại có cần tạo lại không?
15. So sánh Chroma với FAISS (ở project 01).

- Embedding là một vector số học biểu diễn ý nghĩa của dữ liệu. OpenAIEmbeddings được dùng để tạo embedding vetor cho các chunk.

- Chroma.from_documents thực hiện các việc sau: nhận chunk, tạo embedding vector cho các chunk và lưu vào vector store.

- Thư mục chroma_db lưu trữ dữ liệu vector embedding của các chunk. Khi chạy lại nếu dữ liệu ko thay đổi thì ko cần tạo lại.

- So sánh Chroma và FAISS: Chroma là một vector store được phát triển bởi ChromaDB, có thể lưu trữ dữ liệu trên đĩa và hỗ trợ nhiều tính năng như tìm kiếm theo vector, phân loại, clustering,... trong khi đó FAISS là một thư viện mã nguồn mở của Facebook, tập trung vào việc tìm kiếm vector nhanh chóng và hiệu quả.

## Phần 5: Retriever

16. `as_retriever()` trả về gì? Cách đặt số lượng kết quả `k`?
17. Retriever tìm tài liệu liên quan bằng cách nào (độ tương đồng vector)?
18. Điều gì xảy ra khi câu hỏi chứa nhiều ý (multi-hop)? Vì sao retriever dễ thất bại?

- as_retriever() trả về một retriver object dùng để tìm kiếm các chunk liên quan đến câu hỏi. Số lượng kết quả K có thể đặt bằng cách truyền tham số `k` vào hàm.

- Retriver tìm tài liệu liên quan bằng cách tính số độ tương đồng vector giữa embedding của câu hỏi và embedding của các chunk, sau đó trả về các chunk có độ tương đồng cao nhất.

- Khi câu hỏi chứa nhiều ý , retriver dễ thất bại vì nó chỉ tìm kiếm các chunk liên quan đến tổng thể câu hỏi, mà không phân tích được riêng lẻ.

## Phần 6: Tiện ích & cấu hình

19. File `.env` dùng để làm gì? Vì sao không hard-code API key?
20. `format_qa_pair` và `format_qa_pairs` trong `utils.py` làm gì? Dùng ở bước nào của decomposition?

- format_qa_pair và format_qa_pairs trong utils.py dùng để định dạng câu hỏi và câu trả lời.

## Phần 7: Thực hành

21. Viết lại luồng: WebBaseLoader -> Splitter -> Chroma -> Retriever bằng code, không nhìn tài liệu.
22. Thử đổi chunk size (200, 500) và so sánh kết quả truy xuất cho cùng một câu hỏi.
23. Thử một câu hỏi phức tạp, quan sát các chunk trả về và nhận xét chất lượng.
24. Đề xuất cách chia câu hỏi phức tạp thành các câu hỏi con.

- loader = WebBaseLoader(urls=["https://example.com"])
  document = loader.load()
  splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(300, 50)
  splits = splitter.split_documents(document)
  vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings(), persist_directory="./chroma_db")
  retriever = vectorstore.as_retriever()
