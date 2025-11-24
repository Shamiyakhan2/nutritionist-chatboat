from langchain.chains import RetrievalQA
from langchain_community.llms import HuggingFacePipeline
from transformers import pipeline

from retrieval import build_vectorstore
from utils import load_rules


def get_chatbot():
    model_name = "google/flan-t5-small"  
    pipe = pipeline("text2text-generation", model=model_name, max_length=512)
    llm = HuggingFacePipeline(pipeline=pipe)

    vectordb = build_vectorstore()
    if vectordb is None:
       
        def simple_qa(question):
            return "I couldn't access my knowledge base, but generally speaking, nutrition is important for health."
        return simple_qa

    retriever = vectordb.as_retriever()

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=False
    )
    return qa



