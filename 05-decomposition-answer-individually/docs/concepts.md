# Khái niệm: Answer individually

## Là gì
Hàm `retrieve_and_rag(prompt_rag, sub_questions)`.

## Mục đích
Trả lời từng câu hỏi con độc lập bằng prompt RAG chuẩn `hub.pull("rlm/rag-prompt")`.

## Luồng
for sub_question: retriever lấy docs -> prompt_rag | llm | parser -> trả về (answers, questions)

## Bạn học được
- So sánh đệ quy vs độc lập
- Có thể chạy song song (batch)
- Trade-off tốc độ và độ liên kết giữa các câu trả lời

## Việc cần làm
- [ ] Tự implement theo luồng trên
