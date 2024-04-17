from langchain_community.llms import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

from langchain_core.prompts import ChatPromptTemplate

from langchain_core.output_parsers import StrOutputParser

from langchain_community.document_loaders import WebBaseLoader

from langchain_community.embeddings import OllamaEmbeddings

from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

from langchain_community.document_loaders import UnstructuredXMLLoader




output_parser = StrOutputParser()


# prompt = ChatPromptTemplate.from_messages([
#     ("system", "You are a world class technical documentation writer."),
#     ("user", "{input}")
# ])



llm = Ollama(model="llama2:7b-chat-q4_0", 
             callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]))

# chain = prompt | llm | output_parser

# chain.invoke({"input": "how can langsmith help with testing?"})


# loader = WebBaseLoader("https://www.espn.com/")

# docs = loader.load()
loader = UnstructuredXMLLoader(
    "/Users/jacksusank/Downloads/GrantsDBExtract20240310v2.xml",
)

docs = loader.load()
docs[0]


embeddings = OllamaEmbeddings()

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

response = retrieval_chain.invoke({"input": "What's the score of the Colorado State vs  Texas March Madness Basketball game right now?"})
print(response["answer"])

# LangSmith offers several features that can help with testing:...


# Open AI API key: