# Part 3: Trả lời độc lập (tối ưu)

Mỗi câu hỏi con được trả lời riêng, không phụ thuộc Q&A trước; có thể chạy song song.

## Bạn sẽ học
- So sánh đệ quy vs độc lập
- batch / parallel
- Trade-off tốc độ và chất lượng

## Cấu trúc
- `query.py: answer_individually(sub_questions) dùng chain.batch()`
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
