from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import UnstructuredXMLLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_openai import OpenAIEmbeddings
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv



llm = ChatOpenAI(openai_api_ke)

from langchain_core.prompts import ChatPromptTemplate
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are world class technical documentation writer."),
    ("user", "{input}")
])

chain = prompt | llm 

# chain.invoke({"input": "how can langsmith help with testing?"})

from langchain_core.output_parsers import StrOutputParser

output_parser = StrOutputParser()

chain = prompt | llm | output_parser

# chain.invoke({"input": "how can langsmith help with testing?"})

print("spot 1")

class StructuredXMLLoader:
    def __init__(self, file_path):
        with open(file_path, 'r') as file:
            content = file.read()
        self.soup = BeautifulSoup(content, features='xml')

    def load(self):
        return {tag.name: tag.text.strip() for tag in self.soup.find_all()}
loader = StructuredXMLLoader(
    "test.xml",
)

print("spot 2")

docs = loader.load()
print("spot 3")

print(docs.keys())
print("spot 4")
print(docs["OpportunityID"])


embeddings = OpenAIEmbeddings(openai_api_ke)

text_splitter = RecursiveCharacterTextSplitter()
documents = text_splitter.split_documents(docs)
vector = FAISS.from_documents(documents, embeddings)


prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:

<context>
{context}
</context>

Question: {input}""")

document_chain = create_stuff_documents_chain(llm, prompt)

retriever = vector.as_retriever()
retrieval_chain = create_retrieval_chain(retriever, document_chain)

# response = retrieval_chain.invoke({"input": "how can langsmith help with testing?"})
# print(response["answer"])