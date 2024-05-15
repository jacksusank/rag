from dotenv import load_dotenv
import openai
from openai import OpenAI
import psycopg2


load_dotenv()


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


possible_question = "What funding opportunity should I apply for if I have a nonprofit that fosters community and healthy communication amongst Americans by offering them a free online platform to talk with other people like them about their struggles? Currently, we serve groups including independent artists, mothers, and gay men under the age of 35. I'm looking for at least a 100,000 dollar grant. The opportunity must be specifically looking for organizations that support mothers, gay people, or independent artists like mine does."
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
