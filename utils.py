# import

# def load_documents(folder_path: str) -> List[Document]:
#   documents = []
#   for filename in os.listdir(folder_path):
#     # print("filename: ", filename)
#     file_path = os.path.join(folder_path, filename)
#     if(filename.endswith('.pdf')):
#       loader = PyPDFLoader(file_path)
#     elif(filename.endswith('.docx')):
#       loader = Docx2txtLoader(file_path)
#     else:
#       print(f"Unsupported file type: {filename}")
#       continue
#     documents.extend(loader.load())
#   return documents

# folder_path = "../docs"
# documents = load_documents(folder_path)
# print(f"Loaded {len(documents)} documents from the folder.")



# def load_and_split_document(file_path: str) -> List[Document]:
#   if file_path.endswith('.pdf'):
#     loader = PyPDFLoader(file_path)
#   elif file_path.endswith('.docx'):
#     loader = Docx2txtLoader(file_path)
#   elif file_path.endswith('.html'):
#     loader = UnstructuredHTMLLoader(file_path)
#   else:
#     raise ValueError(f"Unsupported file type: {file_path}")
  
#   documents = loader.load()
#   return text_splitter.split_documents(documents)