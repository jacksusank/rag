import json
import xml.etree.ElementTree as ET

from dotenv import load_dotenv

load_dotenv()


# Load the dictionaries
def load_json():
    with open("MyDictionaries.json") as json_file:
        data = json.load(json_file)
    return data


my_dictionaries = load_json()
docs = []


class CustomXMLLoader:
    def load(self, file_path: str):
        badSet = {"Version", "GrantorContactEmailDescription"}
        tree = ET.parse(file_path)
        root = tree.getroot()
        for child in root:
            archive_date = child.find(
                "{http://apply.grants.gov/system/OpportunityDetail-V1.0}ArchiveDate"
            )
            if archive_date is not None and archive_date.text is not None:
                if int(archive_date.text[-4:]) < 2024:
                    print("Old Archive Date: " + archive_date.text)
                    continue
            close_date = child.find(
                "{http://apply.grants.gov/system/OpportunityDetail-V1.0}CloseDate"
            )
            if close_date is not None and close_date.text is not None:
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
                        myString += "The " + thisTag + " is " + subchild.text + ". "
                        # print(subchild.tag)
                    else:
                        print("Something went wrong")
                        print(subchild.text)
                        print(thisTag)
                else:
                    myString += "The " + thisTag + " is " + subchild.text + ". "
                    # print(subchild.tag)

            metadata = {"ID": opportunityID}
            doc = {"page_content": myString, "metadata": metadata}
            docs.append(doc)
        return docs


xml_file_path = "GrantsDBExtract20240310v2.xml"
# xml_file_path = "test.xml"
loader = CustomXMLLoader()
documents = loader.load(xml_file_path)

# documents = documents[:1000]
print(len(documents))
page_contents_list = [doc["page_content"] for doc in documents]
metadata = [doc["metadata"] for doc in documents]


# client = OpenAI()
# response = client.embeddings.create(
#   model="text-embedding-3-small",
#   input=page_contents_list,
#   encoding_format="float"
# )

# # Extract embeddings from the response
# embeddings = response.data

# # Connect to PostgreSQL
# connection = psycopg2.connect(
#     host="localhost",
#     port="5432",
#     database="vector_db",
#     user="postgres",
#     password="test"
# )

# # Create a cursor
# cursor = connection.cursor()

# # Remove contents in the existing collection (table)
# truncate_query = "TRUNCATE TABLE totemembeddings RESTART IDENTITY;"
# cursor.execute(truncate_query)
# connection.commit()


# # Convert embeddings to a suitable format (e.g., list of floats)
# partly_formatted_embeddings = [list(embedding) for embedding in embeddings]
# # fully_formatted_embeddings = [list(part[0])[1:][0] for part in partly_formatted_embeddings]
# fully_formatted_embeddings = [list(part[0])[1] for part in partly_formatted_embeddings]


# print(fully_formatted_embeddings[1])

# # Iterate over fully formatted embeddings, page_content, and metadata and insert them into the database
# for embedding, page_contents, meta in zip(fully_formatted_embeddings, page_contents_list, metadata):
#     # Construct the INSERT query
#     insert_query = """
#     INSERT INTO totemembeddings (embeddings, page_contents, metadata)
#     VALUES (%s, %s, %s);
#     """
#     # Execute the INSERT query
#     cursor.execute(insert_query, (embedding, page_contents, json.dumps(meta)))
#     # Commit the transaction
#     connection.commit()

# # Close cursor and connection
# cursor.close()
# connection.close()
