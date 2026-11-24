# Part 2: Trả lời đệ quy

Hàm generate_qa_pairs(sub_questions): trả lời tuần tự, mỗi câu dùng context + các Q&A trước đó.

## Bạn sẽ học
- itemgetter trong chain
- Kết hợp retrieval + prompt
- Tích lũy q_a_pairs
- format_qa_pair

## Cấu trúc
- `query.py: generate_qa_pairs(sub_questions)`
- `utils.py: format_qa_pair(q, a)`
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
