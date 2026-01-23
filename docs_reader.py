import PyPDF2
import os
class DocumentReader():
    def read_text_file(self,file_path : str):
        """ Read content from a txt file """
        with open(file_path,"r",encoding="utf-8") as f:
            return f.read()
        
    # text = read_text_file("../AI/Practice_streamlit/python_intro.txt")
    # print(text)

    def read_pdf_file(self,file_path : str):
        text = ""
        with open(file_path,"rb") as file:
            pdf_reader = PyPDF2.PdfReader(file)  # object of PyPDF2
            # print(pdf_reader)
            # print(pdf_reader.pages)      # object of pages and it contain list of pages.
            # i = 0   
            for page in pdf_reader.pages:  
                text += page.extract_text() + "\n"
                # if i==0:
                #     print(f" page {i} : {page}")
                #     print(text)
                # i+=1
        return text

    def read_document(self,file_path : str):
        """ Read document content based on file extension """
        _, file_extension = os.path.splitext(file_path)
        # print(" :: ",_)       # it will return root part  
        # print(file_extension)  # it will return ext part 
        file_extension = file_extension.lower()

        if file_extension == ".txt":
            return self.read_text_file(file_path)
        elif file_extension == ".pdf":
            return self.read_pdf_file(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")