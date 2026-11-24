# Part 4: Tổng hợp câu trả lời cuối

Pipeline đầy đủ: sinh câu hỏi con → trả lời từng câu → LLM tổng hợp thành FINAL ANSWER.

## Bạn sẽ học
- Ghép nhiều chain
- CLI hoàn chỉnh
- colorama in màu từng bước

## Cấu trúc
- `main.py: menu + in FINAL ANSWER`
- `query.py: query(user_input) gọi toàn bộ pipeline`
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
