# Part 1: Sinh câu hỏi con (Decomposition)

Hàm generate_sub_questions(query): LLM tách câu hỏi gốc thành 3 câu hỏi con.

## Bạn sẽ học
- Prompt template
- LCEL: prompt | llm | StrOutputParser | split('\n')
- Vì sao tách câu hỏi giúp retrieval tốt hơn

## Cấu trúc
- `query.py: generate_sub_questions(query)`
- `(kế thừa main.py, utils.py từ starter)`
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
