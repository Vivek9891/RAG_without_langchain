import streamlit as st
from vector_store import collection
from embeddings import process_and_add_documents
from memory import History
import os

# ------------------ Streamlit Page Config ------------------
st.set_page_config(
    page_title="RAG Chatbot",
    layout="wide"
)

st.title("📄 RAG Chatbot (PDF + Chat)")
st.write("Ask questions from your documents or chat normally.")

# ------------------ Session State ------------------
if "history_obj" not in st.session_state:
    st.session_state.history_obj = History()
    st.session_state.session_id = st.session_state.history_obj.create_session()
    st.session_state.messages = []

history = st.session_state.history_obj
session_id = st.session_state.session_id

# ------------------ Sidebar: Upload Docs ------------------
st.sidebar.header("📂 Upload Documents")

uploaded_files = st.sidebar.file_uploader(
    "Upload PDF or TXT files",
    type=["pdf", "txt"],
    accept_multiple_files=True
)

if uploaded_files:
    os.makedirs("data", exist_ok=True)

    uploaded_file_paths = []
    for file in uploaded_files:
        file_path = os.path.join("data", file.name)
        with open(file_path, "wb") as f:
            f.write(file.getbuffer())
        
        uploaded_file_paths.append(file_path)

    process_and_add_documents(collection, uploaded_file_paths)
    st.sidebar.success("Documents added to vector store!")

# ------------------ Chat UI ------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask something...")

if user_input:
    # Show user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # Get response
    response, sources = history.conversational_rag_query(
        collection=collection,
        query=user_input,
        session_id=session_id
    )

    # Show assistant message
    with st.chat_message("assistant"):
        st.markdown(response)

        if sources:
            with st.expander("📚 Sources"):
                for s in sources:
                    st.write(s)

    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )
