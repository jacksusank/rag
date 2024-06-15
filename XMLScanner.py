import json

from dotenv import load_dotenv
from lxml import etree

load_dotenv()


# Load the dictionaries
def load_json():
    with open("MyDictionaries.json") as json_file:
        data = json.load(json_file)
    return data


class CustomXMLLoader:
    def load(self, file_path: str):
        docs = []
        my_dictionaries = load_json()
        with open(file_path, "rb") as f:
            xml = f.read()

        root = etree.fromstring(xml)  # type: ignore

        badSet = {"Version", "GrantorContactEmailDescription"}

        for child in root:
            archive_date = child.find(
                "{http://apply.grants.gov/system/OpportunityDetail-V1.0}ArchiveDate"
            )
            if archive_date is not None and archive_date.text is not None:
                if int(archive_date.text[-4:]) < 2024:
                    # print("Old Archive Date: " + archive_date.text)
                    continue
            close_date = child.find(
                "{http://apply.grants.gov/system/OpportunityDetail-V1.0}CloseDate"
            )
            if close_date is not None and close_date.text is not None:
                if int(close_date.text[-4:]) < 2024:
                    # print("Old Close Date: " + close_date.text)
                    continue
            myString = ""
            opportunityID = "Not Found"

            for subchild in child:
                thisTag = subchild.tag.split("}")[-1]
                if thisTag in badSet:
                    # print("BadSet caught")
                    continue
                if thisTag == "OpportunityID":
                    opportunityID = subchild.text
                if thisTag in my_dictionaries:
                    if subchild.text in my_dictionaries[thisTag]:
                        subchild.text = my_dictionaries[thisTag][subchild.text]
                        myString += thisTag + " is " + subchild.text + ". | "
                        # print(subchild.tag)
                    else:
                        print("Something went wrong")
                        print(subchild.text)
                        print(thisTag)
                else:
                    myString += thisTag + " is " + subchild.text + ". | "
                    # print(subchild.tag)

            metadata = {"ID": opportunityID}
            doc = {"page_content": myString, "metadata": metadata}
            docs.append(doc)
        return docs


def read_file():
    xml_file_path = "GrantsDBExtract20240607v2.xml"
    # xml_file_path = "test.xml"
    loader = CustomXMLLoader()
    documents = loader.load(xml_file_path)

    # documents = documents[:1000]
    # print(len(documents))
    return documents
