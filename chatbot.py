import streamlit as st
from langchain.document_loaders import JSONLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_community.llms import HuggingFaceHub

def load_data():
    loader = JSONLoader(
        file_path="translated.json",
        jq_schema='.segments[].text',
        text_content=False
    )
    return loader.load()

def setup_qa_chain():
    docs = load_data()
    embeddings = HuggingFaceEmbeddings()
    db = FAISS.from_documents(docs, embeddings)
    llm = HuggingFaceHub(repo_id="google/flan-t5-large")
    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=db.as_retriever()
    )

def main():
    st.title("Translated Content Chatbot")
    qa_chain = setup_qa_chain()
    
    question = st.text_input("Ask a question about the video content:")
    if question:
        answer = qa_chain.run(question)
        st.text_area("Answer:", value=answer, height=200)

if __name__ == "__main__":
    main()