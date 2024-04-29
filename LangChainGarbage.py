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