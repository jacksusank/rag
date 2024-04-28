# from langchain_openai import ChatOpenAI
# from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv


load_dotenv()

import xml.etree.ElementTree as ET
# from langchain.document_loaders.base import BaseLoader
# from langchain.docstore.document import Document
from typing import List
import json
import openai



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

    def load(self, file_path: str):
        badSet = {"Version", "GrantorContactEmailDescription"}
        tree = ET.parse(file_path)
        root = tree.getroot()
        for child in root:
            archive_date = child.find("{http://apply.grants.gov/system/OpportunityDetail-V1.0}ArchiveDate")
            if archive_date is not None:
                if int(archive_date.text[-4:]) < 2024:
                    print("Old Archive Date: " + archive_date.text)
                    continue
            close_date = child.find("{http://apply.grants.gov/system/OpportunityDetail-V1.0}CloseDate")
            if close_date is not None:
                if int(close_date.text[-4:]) < 2024:
                    print("Old Close Date: " + close_date.text)
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
                if thisTag == "OpportunityID":
                    opportunityID = subchild.text
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
            # doc = Document(page_content=myString, metadata=metadata)
            doc = {"page_content": myString, "metadata": metadata}
            docs.append(doc)
        return docs
    
xml_file_path = "GrantsDBExtract20240310v2.xml"
# xml_file_path = "test.xml"

loader = CustomXMLLoader()
documents = loader.load(xml_file_path)






documents = documents[:1000]
print(len(documents))

# Print the page content of the first doc in documents:
# print(documents[0]['page_content'])
# print(documents[0])

# print(type(documents))
# print(type(documents[0]))
# print(type(documents.page_content.list))

page_contents_list = [doc['page_content'] for doc in documents]


from openai import OpenAI
client = OpenAI()

response = client.embeddings.create(
  model="text-embedding-3-small",
  input=page_contents_list,
  encoding_format="float"
)

# embeddings = response['embeddings']
metadata = [doc['metadata'] for doc in documents]

import psycopg2

# Connect to PostgreSQL
connection = psycopg2.connect(
    host="localhost",
    port="5432",
    database="vector_db",
    user="postgres",
    password="test"
)

# Create a cursor
cursor = connection.cursor()

# Truncate the existing collection (table)
truncate_query = "TRUNCATE TABLE totemembeddings RESTART IDENTITY;"
cursor.execute(truncate_query)
connection.commit()

# Extract embeddings from the response
embeddings = response.data

# print(type(embeddings))
# print(type(embeddings[0]))

# Convert embeddings to a suitable format (e.g., list of floats)
partly_formatted_embeddings = [list(embedding) for embedding in embeddings]



fully_formatted_embeddings = [list(part[0])[1:][0] for part in partly_formatted_embeddings]






# print(fully_formatted_embeddings[1])

# Iterate over formatted embeddings, page_content, and metadata and insert them into the database
for embedding, page_contents, meta in zip(fully_formatted_embeddings, page_contents_list, metadata):
#     # Construct the JSON object
#     embedding_json = {"embedding": formatted_embedding}

#     # Convert the JSON object to a JSON string
#     embedding_json_str = json.dumps(formatted_embedding)

    # Convert formatted_embedding to a suitable format (e.g., string)
    # formatted_embedding_str = ','.join(map(str, formatted_embedding))

    # Construct the INSERT query
    insert_query = """
    INSERT INTO totemembeddings (embeddings, page_contents, metadata)
    VALUES (%s, %s, %s);
    """
    # Execute the INSERT query
    cursor.execute(insert_query, (embedding, page_contents, json.dumps(meta)))
    # Commit the transaction
    connection.commit()

# Close cursor and connection
cursor.close()
connection.close()




def findSimilarVectors(user_tuple):
    # Connect to PostgreSQL
    connection = psycopg2.connect(
        host="localhost",
        port="5432",
        database="vector_db",
        user="postgres",
        password="test"
    )

    # Create a cursor
    cursor = connection.cursor()
    # Perform similarity search
    insert_query = """
    SELECT page_contents, (embeddings <=> (%s::vector)) AS cosine_distance
    FROM totemembeddings
    ORDER BY cosine_distance
    LIMIT 2;
    """

    cursor.execute(insert_query, (user_tuple[0],))

    # Fetch and process the results
    results = cursor.fetchall()
    output = ""
    i = 0
    choices = ["one", "another", "yet another", "another"]
    for row in results:
        page_contents, similarity_score = row
        output += ("This is " + choices[i] + " relevant opportunity:\n")
        output += (str(page_contents))
        # print("Page Contents: ", page_contents)
        # print("Similarity Score: ", similarity_score)
        i += 1

    # Close cursor and connection
    cursor.close()
    connection.close()

    return user_tuple[1] + output




def promptMaker(input):
    output = f"You are a world class advisor to nonprofits who are seeking to find the most appropriate RFPs \
        (request for proposals) for their organization to apply for. You will be given the user's query followed \
            by some relevant context. You should use the context to answer the user's query. You should always \
                include the relevant opportunity ID in your response. Here is the query and context: {input}"


    return output




def chatWithLLM(my_prompt):
    # # Query ChatGPT
    # response = openai.Completion.create(
    #     engine="text-embedding-3-small", 
    #     prompt=my_prompt,
    #     max_tokens=10000,  # Maximum length of the completion
    #     # temperature=0.7,  # Controls randomness of the completion
    #     stop=["\n"]  # Stop generation at the end of the conversation
    # )
    # return response.choices[0].text.strip()
    print(my_prompt)
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",  # Choose the GPT model,
        messages=[{"role": "user", "content": my_prompt}]
    )

    return response.choices[0].message.content

# chain = findSimilarVectors | prompt | chatWithLLM()

possible_question = "What funding opportunity should I apply for if my organization serves to find innovative solutions to challenging public health problems?"

while (input != "quit"):
    # my_input = str(input("Enter a query: "))
    my_input = possible_question
    print("\n\nResults: ")

    client = OpenAI()

    response = client.embeddings.create(
    model="text-embedding-3-small",
    input=my_input,
    encoding_format="float"
    )

    embedded_input = response.data

    partly_formatted_input = [list(embedding) for embedding in embedded_input]

    fully_formatted_input = [list(part[0])[1:][0] for part in partly_formatted_input]


    print(chatWithLLM(promptMaker(findSimilarVectors((fully_formatted_input[0], my_input)))))
    # print(chain.invoke(my_input))
    print("\n\n")

    input = "quit"




















# from pgvector.django import L2Distance




# embedded_prompt = client.embeddings.create(
#   model="text-embedding-3-small",
#   input=prompt,
#   encoding_format="float"
# )
# def getInput(query):
#     input = ["Query: " + query]
#     context = embeddings.objects.order_by(L2Distance('embedding',embedded_prompt))

#     input.append(context)

# embeddings.objects.order_by(L2Distance('embedding', [1, 2, 3]))

# # Define the prompt and the completion parameters
# completion_parameters = {
#     "model": "text-embedding-3-small",  # Model name or ID
#     "max_tokens": 50  # Maximum number of tokens in the completion
# }

# # Query the GPT model
# response = openai.Completion.create(prompt=prompt, **completion_parameters)

# # Print the generated text
# print(response.choices[0].text.strip())

# llm = ChatOpenAI()


# chain = getSimilar | prompt | llm

# chain.invoke("Enter a query: ")


# embedded_prompt = client.embeddings.create(
#   model="text-embedding-3-small",
#   input=prompt,
#   encoding_format="float"
# )







# # embeddings = OpenAIEmbeddings(model="text-embedding-3-small")


# # from langchain.vectorstores.pgvector import PGVector
# # CONNECTION_STRING = "postgresql+psycopg2://postgres:test@localhost:5432/vector_db"
# # COLLECTION_NAME = 'grants_vectors_1'

# # db = PGVector.from_documents(embedding=embeddings, documents=documents, collection_name=COLLECTION_NAME, connection_string=CONNECTION_STRING, pre_delete_collection=True)

# from pgvector import PGVector
# from pgvector.django import L2Distance

# Item.objects.order_by(L2Distance('embedding', [1, 2, 3]))


# def getSimilar(query):
#     similar = ["Query: " + query]
#     similar.append(db.similarity_search_with_score(query, k=1))

#     return similar


# llm = ChatOpenAI()

# from langchain_core.prompts import ChatPromptTemplate
# prompt = ChatPromptTemplate.from_messages([
#     ("system", """You are a world class advisor to nonprofits who are seeking to find the most appropriate RFPs (request for proposals) for their organization to apply for. 
#      You will be given the user's query followed by some relevant context.
#      You should use the context to answer the user's querry.
#      You should always include the relevant opportunity ID in your response."""),
#     ("user", "{input}")
# ])


# chain = getSimilar | prompt | llm

# while (input != quit):
#     my_input = str(input("Enter a query: "))
#     print(type(my_input))
#     print("\n\nResults: ")
#     print(chain.invoke(my_input))
#     print("\n\n")