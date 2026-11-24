# Khái niệm: Final answer

## Là gì
Hoàn thiện `query()` và `main.py`.

## Mục đích
Ghép toàn bộ pipeline và tổng hợp câu trả lời cuối.

## Luồng
generate_sub_questions -> retrieve_and_rag -> format_qa_pairs(questions, answers) -> prompt | llm | parser (context, question) -> FINAL ANSWER

## Bạn học được
- Ghép nhiều chain thành ứng dụng
- CLI menu và vòng lặp hỏi đáp
- Dùng colorama in màu từng bước

## Việc cần làm
- [ ] Tự implement theo luồng trên
