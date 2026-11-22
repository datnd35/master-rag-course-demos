import gc
import json
import os
import shutil
import warnings

from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from colorama import Fore

warnings.filterwarnings("ignore")

# Đọc biến môi trường từ file .env (vd: OPENAI_API_KEY)
load_dotenv()

# Khởi tạo model chat mặc định của OpenAI
model = ChatOpenAI()


def reset_vectorstore():
    global vectorstore, documents, chunks, embeddings

    # Clear RAM
    vectorstore = None
    documents = []
    chunks = []
    embeddings = None

    # Delete old FAISS data
    if os.path.exists("faiss_index"):
        shutil.rmtree("faiss_index")

    # Garbage collection
    gc.collect()

    print("Reset completed! Ready to ingest documents again.")


# RESET DATA BEFORE INGESTION
reset_vectorstore()


# BƯỚC 1: Tải tài liệu từ web (giống "tải sách về máy")
loader = WebBaseLoader(
    "https://python.langchain.com/docs/get_started/introduction"
)

documents = loader.load()

# In thông tin debug: số tài liệu, metadata, độ dài, đoạn xem trước
print("\n===== DOCUMENT LOADER DEBUG =====")
print("Number of documents:", len(documents))

for i, doc in enumerate(documents):
    print(f"\nDocument {i + 1}")
    print("Metadata:", doc.metadata)
    print("Content length:", len(doc.page_content))
    print("Content preview:")
    print(doc.page_content[:1000])

#print documents
# print(Fore.GREEN + "Documents loaded from the web:")
# for doc in documents:
#     print(Fore.YELLOW + doc.page_content[:500] + "...")  # Print the first 500 characters of each document


# Mẫu prompt: {question} là câu hỏi, {context} là các đoạn tài liệu tìm được
# (Lưu ý: prompt này chưa được truyền vào chain bên dưới)
template = """You are a senior developer who answers {question} base on your knowledge and {context}."""

prompt = PromptTemplate(
    template=template,
    input_variables=["question", "context"]
)

# BƯỚC 2: Cắt tài liệu dài thành nhiều đoạn nhỏ (chunk) ~1000 ký tự,
# mỗi đoạn gối đầu 200 ký tự để không mất ngữ cảnh ở chỗ cắt
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = text_splitter.split_documents(documents)

print("Total chunks:", len(chunks))

# BƯỚC 3: Chuyển mỗi chunk thành vector (dãy số biểu diễn ý nghĩa) qua OpenAI,
# rồi lưu vào FAISS (kho vector, nằm trong RAM)
embeddings = OpenAIEmbeddings()

vectorstore = FAISS.from_documents(
    chunks,
    embeddings
)

# BƯỚC 4: Lưu FAISS ra đĩa (index.faiss + index.pkl) để lần sau không phải embed lại
os.makedirs("faiss_index", exist_ok=True)

vectorstore.save_local("faiss_index")


# Xuất nội dung + metadata của từng chunk ra index.json cho dễ đọc
metadata = {"chunks": []}

for i in range(vectorstore.index.ntotal):

    doc_id = vectorstore.index_to_docstore_id[i]
    doc = vectorstore.docstore.search(doc_id)

    metadata["chunks"].append({
        "id": str(doc_id),
        "text": doc.page_content,
        "source": doc.metadata.get("source", ""),
        "metadata": doc.metadata
    })

with open("faiss_index/index.json", "w") as f:
    json.dump(metadata, f, indent=2, ensure_ascii=False, default=str)

print("FAISS and metadata exported successfully!")


# Hàm trả lời câu hỏi: tìm đoạn liên quan -> đưa cho LLM -> trả về câu trả lời
def generate_response(query: str):

    # Bước 1: Retrieve - tìm 3 chunk giống câu hỏi nhất
    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 3}
    )

    retrieved_docs = retriever.invoke(query)

    print("\n===== RETRIEVER DEBUG =====")

    for i, doc in enumerate(retrieved_docs):
        print(f"\nDocument {i + 1}:")
        print(doc.page_content[:500])

    # Bước 2: Generate - "nhồi" (stuff) các chunk vào prompt rồi để gpt-4o-mini trả lời
    # temperature=0 để câu trả lời ổn định, ít sáng tạo
    chain = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0
        ),
        retriever=retriever,
        chain_type="stuff",
        return_source_documents=True
    )

    response = chain.invoke({"query": query})

    print("\n===== SOURCE DOCUMENTS =====")
    print("Sources:", len(response["source_documents"]))

    return response["result"]

# Menu chính: 1 = đặt câu hỏi, 2 = thoát
def start():
    instructions = Fore.GREEN + "Welcome to the LangChain QA System! You can ask questions about LangChain, and I'll provide answers based on the loaded documents."
    print(instructions)

    choice = input(Fore.CYAN + "Type '1' to ask a question or '2' to quit: ")
    if choice.lower() == '1':
        ask()
    elif choice.lower() == '2':
        print(Fore.GREEN + "Exiting the QA system. Goodbye!")
    else:
        print(Fore.RED + "Invalid choice. Please try again.")
        start()

# Vòng lặp hỏi đáp: gõ 'x' để quay lại menu (dù hint ghi 'exit')
def ask():
   while True:
       user_input = input(Fore.CYAN + "Ask a question (or type 'x' to quit): ")
       if user_input == 'x':
             start()
       else:
           response = generate_response(user_input)
           print(Fore.YELLOW + "Response: " + response) 


# Điểm bắt đầu khi chạy: python main.py
if __name__ == "__main__":
    start() 