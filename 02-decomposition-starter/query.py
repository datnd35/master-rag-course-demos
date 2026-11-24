"""Logic RAG: chỉ đọc vector store đã ingest (chạy `python ingest.py` trước)."""

import warnings

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from colorama import Fore
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_openai import ChatOpenAI

from utils import get_vectorstore

warnings.filterwarnings("ignore")
load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")
retriever = get_vectorstore().as_retriever(search_kwargs={"k": 4})

prompt = PromptTemplate.from_template(
    "Answer the question using only the context below.\n\n"
    "Context:\n{context}\n\nQuestion: {question}\nAnswer:"
)
chain = prompt | llm | StrOutputParser()


#Decomposition 
template = """You are a helpful assistant that answers questions based on the provided context.
 If the question is complex, break it down into simpler sub-questions and answer them step by step. 
 Use the context to support your answers. If the answer is not found in the context,
 respond with 'I don't know.'\n\nContext:\n{context}\n\nQuestion: {question}\nAnswer:"""

prompt_decomposition = PromptTemplate.from_template(template);

def generate_sub_questions(question: str):
    """ generate sub questions based on user query"""
    pass
    
    #chain
    generate_queries_decomposition = prompt_decomposition | llm | StrOutputParser() | (lambda x: x.split("\n") ) 

    #run
    sub_questions = generate_queries_decomposition.invoke({"question": question})
    questions_str = "\n".join(sub_questions)
    print(f"{Fore.GREEN}Sub-questions: {questions_str}")


# 2. ANSWER SUBQUESTIONS RECURSIVELY 
template = """Here is the question you need to answer:

\n --- \n {sub_question} \n --- \n

Here is any available background question + answer pairs:

\n --- \n {q_a_pairs} \n --- \n

Here is additional context relevant to the question: 

\n --- \n {context} \n --- \n

Use the above context and any background question + answer pairs to answer the question: \n {sub_question}
"""
prompt_qa = ChatPromptTemplate.from_template(template)


def generate_qa_pairs(sub_questions):
    """ ask the LLM to generate a pair of question and answer based on the original user query """
    pass
    

# 3. ANSWER INDIVIDUALLY

# RAG prompt = https://smith.langchain.com/hub/rlm/rag-prompt
prompt_rag = ChatPromptTemplate.from_template(
    "You are an assistant for question-answering tasks. Use the following context "
    "to answer the question. If you don't know, say so. Keep it concise.\n"
    "Question: {question}\nContext: {context}\nAnswer:"
)


def retrieve_and_rag(prompt_rag, sub_questions):
    """RAG on each sub-question"""
    pass
    


# SUMMARIZE AND ANSWER 

# Prompt
template = """Here is a set of Q+A pairs:

{context}

to use these to synthesize an answer to the question: {question}
"""

prompt = ChatPromptTemplate.from_template(template)

def query(question: str) -> str:
    context_docs = retriever.invoke(question)
    context = "\n\n".join(d.page_content for d in context_docs)
    return chain.invoke({"context": context, "question": question})