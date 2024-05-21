# Queries the database with the user's question and returns the 4 most similar opportunities

from dotenv import load_dotenv
import openai
import psycopg2
from sentence_transformers import SentenceTransformer
import sys

import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
if __name__ == "__main__":
    query = sys.argv[1]
    my_input = query

load_dotenv()

def findSimilarVectors(user_tuple):
    """
    This function performs a similarity search on the database and returns the page content of the 4 opportunities that are most similar to the user's ideal RFP

    Args:
        user_tuple (tuple): A tuple containing the vectorized version of the fake RFP that was created and the user's query (vectorized fake rfp, query)

    Returns:
        str: A string containing the original question that was asked by the user followed by the page content of the 4 most similar opportunities
    """
    # Generic connection to PostgreSQL
    connection = psycopg2.connect(
        host="localhost",
        port="5432",
        database="totem",
        user="postgres"
    )

    # Create a cursor
    cursor = connection.cursor()

    # Perform cosine similarity search
    # Returns the page contents of the 4 most similar opportunities
    insert_query = """
    SELECT page_contents, (embeddings <=> (%s::vector)) AS cosine_distance
    FROM totemembeddings
    ORDER BY cosine_distance
    LIMIT 4;
    """

    cursor.execute(insert_query, (user_tuple[0],))

    # Fetch and process the results
    results = cursor.fetchall()
    output = ""
    i = 0
    choices = ["one", "another", "yet another", "another"]
    for row in results:
        page_contents, similarity_score = row
        intro = ("Here are the details of " + choices[i] + " relevant opportunity with a similarity score of " + str(similarity_score) + ":\n")
        output += intro 
        output += (str(page_contents) + "\n")
        # print("Page Contents: ", page_contents)
        # print("Similarity Score: ", similarity_score)
        i += 1

    # Close cursor and connection
    cursor.close()
    connection.close()

    return user_tuple[1] + output


def promptMaker(input):
    """
    This function creates a prompt for the LLM model to respond to

    Args:
        input (str): The output of the findSimilarVectors function (the original question followed by the page content of the 4 most similar opportunities)

    Returns:
        str: A string containing the prompt that the LLM model will respond to
    """
    output = f"You are a world class advisor to nonprofits who are seeking to find the most appropriate RFPs \
        (request for proposals) for their organization to apply for. You will be given the user's query followed \
            by some relevant context. You should use the context to answer the user's query. You should always \
                include the relevant opportunity ID in your response. You should list at least one opportunity that \
                    would be good for the user to apply for, but list more if the opportunities are worth looking into.\
                        Here is the query and context: {input}"

    return output


def chatWithLLM(my_prompt):
    """
    This function uses GPT-3.5-turbo to respond to a prompt

    Args:
        my_prompt (str): The prompt that the LLM model will respond to (the output of the promptMaker function)
    
    Returns:
        str: The response from the LLM model
    """
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",  # Choose the GPT model,
        messages=[{"role": "user", "content": my_prompt}]
    )
    return response.choices[0].message.content


# possible_question = "What funding opportunity should I apply for if I have a nonprofit that fosters community and healthy communication amongst Americans by offering them a free online platform to talk with other people like them about their struggles? We do not conduct research but we currently serve groups including independent artists, mothers, and gay men under the age of 35. I'm looking for at least a 100,000 dollar grant. The opportunity must be specifically looking for organizations that support mothers, gay people, or independent artists like mine does. We are helping people with their mental and emotional health. We are basically a virtual version of alcoholics anonymous in that we offer an alternative to traditional therapy and western medicine. We also facilitate healthy conversations by using a native american technique involving a totempiece that rotates clockwise around the circle indicating who is allowed to talk. We do not conduct research of any kind! We offer mental health services through community support platforms."

# First, we need to create a fake RFP that would be perfect for the user's question so that the similarity search can be performed
ideal_opportunity = chatWithLLM("I want you to create a fake RFP that would be perfect for someone who has this question:" + my_input + ". \nI want you to do it in the following format: The OpportunityTitle is (Title). The OpportunityCategory is (Category). The FundingInstrumentType is (Funding Instrument Type). The CategoryOfFundingActivity is (Category Of Funding Activity). The EligibleApplicants is (Applicants). The AdditionalInformationOnEligibility is (Additional Info like a description). The AgencyName is (Agency Name)). The Description is (Description).")
print(ideal_opportunity)

# Next, we need to vectorize the fake RFP so that it can be compared to the other opportunities in the database
model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
vectorized_ideal_opportunity = model.encode(ideal_opportunity)
print(type(vectorized_ideal_opportunity))
print(len(vectorized_ideal_opportunity))
fully_formatted_ideal_opportunty = [embedding.tolist() for embedding in vectorized_ideal_opportunity]

# Now, we can perform the similarity search, turning the output into a prompt and then passing this into the LLM model
print("\n\nResults: ")
llmResponse = (chatWithLLM(promptMaker(findSimilarVectors((fully_formatted_ideal_opportunty, my_input)))))
print(llmResponse)

my_input = "quit"
