from dotenv import load_dotenv
import xml.etree.ElementTree as ET
import json
import openai
from openai import OpenAI
import psycopg2

load_dotenv()

# Load the dictionaries
def load_json():
    with open('MyDictionaries.json') as json_file:
        data = json.load(json_file)
    return data

my_dictionaries = load_json()
docs = []

class CustomXMLLoader():
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
            doc = {"page_content": myString, "metadata": metadata}
            docs.append(doc)
        return docs
    
xml_file_path = "GrantsDBExtract20240310v2.xml"
# xml_file_path = "test.xml"
loader = CustomXMLLoader()
documents = loader.load(xml_file_path)


documents = documents[:1000]
page_contents_list = [doc['page_content'] for doc in documents]
metadata = [doc['metadata'] for doc in documents]

client = OpenAI()
response = client.embeddings.create(
  model="text-embedding-3-small",
  input=page_contents_list,
  encoding_format="float"
)

# Extract embeddings from the response
embeddings = response.data

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

# Remove contents in the existing collection (table)
truncate_query = "TRUNCATE TABLE totemembeddings RESTART IDENTITY;"
cursor.execute(truncate_query)
connection.commit()


# Convert embeddings to a suitable format (e.g., list of floats)
partly_formatted_embeddings = [list(embedding) for embedding in embeddings]
# fully_formatted_embeddings = [list(part[0])[1:][0] for part in partly_formatted_embeddings]
fully_formatted_embeddings = [list(part[0])[1] for part in partly_formatted_embeddings]


print(fully_formatted_embeddings[1])

# Iterate over fully formatted embeddings, page_content, and metadata and insert them into the database
for embedding, page_contents, meta in zip(fully_formatted_embeddings, page_contents_list, metadata):
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
    # Perform cosine similarity search
    insert_query = """
    SELECT page_contents, (embeddings <=> (%s::vector)) AS cosine_distance
    FROM totemembeddings
    ORDER BY cosine_distance
    LIMIT 3;
    """

    cursor.execute(insert_query, (user_tuple[0],))

    # Fetch and process the results
    results = cursor.fetchall()
    output = ""
    i = 0
    choices = ["one", "another", "yet another", "another"]
    for row in results:
        page_contents, similarity_score = row
        my_string = ("Here are the details of " + choices[i] + " relevant opportunity with a similarity score of " + str(similarity_score) + ":\n")
        output += my_string 
        output += (str(page_contents) + "\n")
        similarOpportunities[i] += my_string
        similarOpportunities[i] += (str(page_contents))
        # print("Page Contents: ", page_contents)
        # print("Similarity Score: ", similarity_score)
        i += 1

    # Close cursor and connection
    cursor.close()
    connection.close()

    # Returns a string containing the original question that was asked by the user followed by the page
    # content of the 3 most similar opportunities (3 becayse we specified LIMIT 3 in the query)
    return user_tuple[1] + output


def promptMaker(input):
    output = f"You are a world class advisor to nonprofits who are seeking to find the most appropriate RFPs \
        (request for proposals) for their organization to apply for. You will be given the user's query followed \
            by some relevant context. You should use the context to answer the user's query. You should always \
                include the relevant opportunity ID in your response. Here is the query and context: {input}"

    return output

def chatWithLLM(my_prompt):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",  # Choose the GPT model,
        messages=[{"role": "user", "content": my_prompt}]
    )
    return response.choices[0].message.content

def followUpQuestions(questionAndHistory):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",  # Choose the GPT model,
        messages=[{"role": "user", "content": questionAndHistory}]
    )
    return response.choices[0].message.content


possible_question = "What funding opportunity should I apply for if I have a 501c(3) nonprofit that fosters community and healthy communication amongst Americans by offering them a free online platform to talk other people like about their struggles? Currently, we serve communities including independent artists, mothers, and gay men under the age of 35. I'm looking for at least a 100,000 dollar grant. The opportunity must be specifically looking for organizations that support mothers, gay people, or independent artists like mine does."
my_input = ""
while (my_input != "quit"):
    # my_input = str(input("Enter a query: "))
    my_input = possible_question
    
    client = OpenAI()
    vectorized_question = client.embeddings.create(
    model="text-embedding-3-small",
    input=my_input,
    encoding_format="float"
    )

    firstOpportunity = ""
    secondOpportunity = ""
    thirdOpportunity = ""
    fourthOpportunity = ""
    similarOpportunities = [firstOpportunity, secondOpportunity, thirdOpportunity, fourthOpportunity]


    embedded_input = vectorized_question.data
    partly_formatted_input = [list(embedding) for embedding in embedded_input]
    fully_formatted_input = [list(part[0])[1] for part in partly_formatted_input]

    print("\n\nResults: ")
    llmResponse = (chatWithLLM(promptMaker(findSimilarVectors((fully_formatted_input[0], my_input)))))
    print(llmResponse)
    print("\n\n")

    old_question = my_input
    my_input = str(input("Do you have any follow up questions? If so, ask them here: "))

    directions = "You are a world class advisor to nonprofits owners who are seeking to find the most appropriate RFPs \
        (request for proposals) for their organization to apply for. You just gave an owner some advice, and now they are asking \
            followup questions. Please answer them to the best of your ability. Here is a log of the conversation that you are in \
                followed by some context and the owner's new question:\n"
    conversation_log = "The owner's old question: " + old_question + "\nYour response to it: " + llmResponse
    context = "Here is some relevent info for you to use as context: " + similarOpportunities[0] + similarOpportunities[1] + similarOpportunities[2] + similarOpportunities[3]
    new_question = "\nThe owner's new question that you are to answer now: " + my_input
    follow_up_prompt = directions + conversation_log + context + new_question

    print(follow_up_prompt)
    print(followUpQuestions(follow_up_prompt))

    # We don't deal with cancer, so that would not be a good fit for us. Do you have any opportunities that are more in line with our mission of offering an alternative to traditional therapy for people with mental health issues?"
    #That's good, but is there an opportunity that is specifically looking to support organizations that support mothers, gay people, or independent artists like mine?

    my_input = "quit"
