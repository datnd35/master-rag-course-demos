# Khái niệm: Answer recursively

## Là gì
Hàm `generate_qa_pairs(sub_questions)`.

## Mục đích
Trả lời tuần tự; mỗi câu dùng context từ retriever và các Q&A đã trả lời trước.

## Luồng
for sub_question: {context: itemgetter("sub_question") | retriever, sub_question, q_a_pairs} | prompt_qa | llm | parser -> format_qa_pair -> nối vào q_a_pairs

## Bạn học được
- `itemgetter` trong chain
- Kết hợp retrieval và prompt
- Tích lũy tri thức qua từng bước
- Ưu: có ngữ cảnh trước; nhược: chậm, lỗi lan truyền

## Việc cần làm
- [ ] Tự implement theo luồng trên
