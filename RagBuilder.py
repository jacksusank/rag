from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv


load_dotenv()

import xml.etree.ElementTree as ET
from langchain.document_loaders.base import BaseLoader
from langchain.docstore.document import Document
from typing import List
import json

# Load the JSON data
def load_json():
    with open('MyDictionaries.json') as json_file:
        data = json.load(json_file)
    return data

my_dictionaries = load_json()

docs = []

class CustomXMLLoader():
    # def __init__(self, file_path: str):
    #     self.loader = BaseLoader(file_path)

    #     super().__init__(file_path, encoding)
        # super().__init__(file_path)  # Pass only the file_path argument to the base class's __init__ method
        # self.encoding = encoding  # Assign the encoding argument to an instance variable if needed

    def load(self, file_path: str) -> List[Document]:
        badSet = {"Version", "GrantorContactEmailDescription"}
        tree = ET.parse(file_path)
        root = tree.getroot()
        for child in root:
            archive_date = child.find("{http://apply.grants.gov/system/OpportunityDetail-V1.0}ArchiveDate")
            if archive_date is not None:
                if int(archive_date.text[-4:]) < 2024:
                    print("Old Date: " + archive_date.text)
                    continue
            myString = ""
            opportunityID = "Not Found"
            for subchild in child:
                thisTag = subchild.tag.split("}")[-1]
                if thisTag in badSet:
                    print("BadSet caught")
                    continue
                # if thisTag == "EligibleApplicants":
                #     if subchild.text == "12":
                #         myString+= "The " + thisTag + " are Nonprofits having a 501 (c) (3) status with the IRS, other than institutions of higher education"
                
                # Replaces the text with the value in the dictionary if the tag is in the dictionary
                if thisTag in my_dictionaries: 
                    if subchild.text in my_dictionaries[thisTag]:
                        subchild.text = my_dictionaries[thisTag][subchild.text]
                        myString+=("The " + thisTag + " is " + subchild.text + ". ")
                        print(subchild.tag)
                    else:
                        print("Something went wrong")
                        print(subchild.text)
                        print(thisTag)
                else:
                    myString+=("The " + thisTag + " is " + subchild.text + ". ")
                    print(subchild.tag)
                    
            metadata = {"ID": opportunityID}
            doc = Document(page_content=myString, metadata=metadata)
            docs.append(doc)
        return docs
    
# xml_file_path = "GrantsDBExtract20240310v2.xml"
xml_file_path = "test.xml"

loader = CustomXMLLoader()
documents = loader.load(xml_file_path)

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")


from langchain.vectorstores.pgvector import PGVector
CONNECTION_STRING = "postgresql+psycopg2://postgres:test@localhost:5432/vector_db"
COLLECTION_NAME = 'grants_vectors_1'

db = PGVector.from_documents(embedding=embeddings, documents=documents, collection_name=COLLECTION_NAME, connection_string=CONNECTION_STRING, pre_delete_collection=True)



def getSimilar(query):
    similar = ["Query: " + query]
    similar.append(db.similarity_search_with_score(query, k=1))

    return similar


llm = ChatOpenAI()

from langchain_core.prompts import ChatPromptTemplate
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a world class advisor to nonprofits who are seeking to find the most appropriate RFPs (request for proposals) for their organization to apply for. 
     You will be given the user's query followed by some relevant context.
     You should use the context to answer the user's querry.
     You should always include the relevant opportunity ID in your response."""),
    ("user", "{input}")
])


chain = getSimilar | prompt | llm

while (input != quit):
    my_input = str(input("Enter a query: "))
    print(type(my_input))
    print("\n\nResults: ")
    print(chain.invoke(my_input))
    print("\n\n")