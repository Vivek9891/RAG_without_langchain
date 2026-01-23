
from text_chunk import TextSplitter
# import docs_reader as dr
from docs_reader import DocumentReader
from vector_store import collection
from embeddings import process_and_add_documents
from semantic import semantic_search, print_search_result,get_context_with_sources
from gemini import LLM
from memory import History
# pdf = read_pdf_file("../AI/Practice_streamlit/intro_python.pdf")
# print(pdf)
# print("-".join([str(i) for i in range(1,10)]))


# obj = DocumentReader()
# text = obj.read_document("../AI/Practice_streamlit/intro_python.pdf")   # path contain(root+ext) 
# print(text)


#---- chunking -----
# splitter = tc.TextSplitter()
# chunks = splitter.split_text(text)
# print(f"length : {len(chunks[0])}")
# chunks = splitter.sentence_aware_text_splitter(text)
# print(f"length : {len(chunks[0])}")

# for i,sp in enumerate(splitter):
#     print(i,sp)
#     print("length : ",len(sp))
# print(len(splitter))

# obj = DocumentReader()
# text1 = obj.read_pdf_file("../AI/pdf_files/company.pdf")
# print(len(text1))
# split1 = TextSplitter()
# chunks1 = split1.split_text(text1)
# print(len(chunks1))


# text2 = obj.read_pdf_file("../AI/pdf_files/intro_python.pdf")
# print(len(text2))
# split2 = TextSplitter()
# chunks2 = split2.split_text(text2)
# print(len(chunks2))

#----------------- process documents in Chromadb
# process_and_add_documents(collection,"../AI/pdf_files")
# print(collection)

# --------------- Sementic search ------------
# query = "who win yesterday cricket match?"
# results = semantic_search(collection,query)
# # print(results) 

# # print_search_result(results) 
# context,sources = get_context_with_sources(results)
# print(context) 

# ask = LLM()
# response = ask.generate_response(context,query)
# print("LLM response :\n\n",response)

obj = History()
session_id = obj.create_session()
print(session_id)

query = "what is python programming"
response, sources = obj.conversational_rag_query(
    collection,
    query,
    session_id
)

query = "please explain it again"
response, sources = obj.conversational_rag_query(
    collection,
    query,
    session_id
)

print("\n\n : ",response)