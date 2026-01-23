# ------------------- Chunking -----------------
from typing import List,Tuple
import re
class TextSplitter:
    def __init__(self,chunk_size: int = 500,chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split_text(self,text: str) -> List[str]:
            chunks = []
            start = 0
            text_length = len(text)

            while start < text_length:
                end = start + self.chunk_size
                chunk = text[start:end]
                chunks.append(chunk)
                start = end - self.chunk_overlap

            return chunks

        # chunks = split_text(text)
        # print("\n\n CHUNKS : ",chunks)
        # print(chunks[0])
        # print(len(chunks[0]))

    def sentence_aware_text_splitter(self,text:str) -> List[str]:
        sentences = re.split(r'(?<=[.!?])\s+', text)
        # for i,sp in enumerate(sentences):
        #     print(i,sp)
        #     print("length : ",len(sp))
        chunks = []
        current_chunk = "" 

        for sentence in sentences:
            if (len(current_chunk) + len(sentence)) <= (self.chunk_size):
                current_chunk += " " + sentence
            else : 
                chunks.append(current_chunk.strip())
                current_chunk = sentence

        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
