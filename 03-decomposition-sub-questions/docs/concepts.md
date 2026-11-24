# Khái niệm: Sub-questions

## Là gì
Hàm `generate_sub_questions(query)`.

## Mục đích
Tách câu hỏi phức tạp thành 3 câu hỏi con có thể trả lời độc lập, để retrieval phủ nhiều khía cạnh hơn.

## Luồng
prompt_decomposition | llm | StrOutputParser() | split("\n") -> in danh sách bằng colorama -> return list

## Bạn học được
- Viết prompt template
- LCEL (toán tử `|`)
- Vì sao decomposition cải thiện retrieval

## Việc cần làm
- [ ] Tự implement theo luồng trên
