from lxml import etree


xml_file_path = "test.xml"

tree = etree.parse(xml_file_path)

root = tree.getroot()

mySet = set()


for child in root:
    print("Tag:", child.tag)
    myString = ""
    # print("Attributes:", child.attrib)  # Attributes dictionary

    # If the element has text content, print it
    for subchild in child:
        if subchild.tag == "OpportunityID":
            print(subchild.tag, subchild.text)
            myString+= ("The " + subchild.tag + " is " + subchild.text + "\n")
        elif subchild.tag == "OpportunityTitle":
            print(subchild.tag, subchild.text)
            myString+= ("The " + subchild.tag + " is " + subchild.text + "\n")
        elif subchild.tag == "OpportunityNumber":
            print(subchild.tag, subchild.text)
            myString+= ("The " + subchild.tag + " is " + subchild.text + "\n")
        elif subchild.tag == "OpportunityCategory":
            print(subchild.tag, subchild.text)
            myString+= ("The " + subchild.tag + " is " + subchild.text + "\n")
        elif subchild.tag == "FundingInstrumentType":
            print(subchild.tag, subchild.text)
            myString+= ("The " + subchild.tag + " is " + subchild.text + "\n")
        elif subchild.tag == "CategoryOfFundingActivity":
            print(subchild.tag, subchild.text)
            myString+= ("The " + subchild.tag + " is " + subchild.text + "\n")
        elif subchild.tag == "CategoryExplanation":
            print(subchild.tag, subchild.text)
            myString+= ("The " + subchild.tag + " is " + subchild.text + "\n")
        elif subchild.tag == "CFDANumbers":
            print(subchild.tag, subchild.text)
            myString+= ("The " + subchild.tag + " is " + subchild.text + "\n")
        elif subchild.tag == "EligibleApplicants":
            print(subchild.tag, subchild.text)
            myString+= ("The " + subchild.tag + " is " + subchild.text + "\n")
        elif subchild.tag == "AdditionalInformationOnEligibility":
            print(subchild.tag, subchild.text)
            myString+= ("The " + subchild.tag + " is " + subchild.text + "\n")
        elif subchild.tag == "AgencyCode":
            print(subchild.tag, subchild.text)
            myString+= ("The " + subchild.tag + " is " + subchild.text + "\n")
        elif subchild.tag == "AgencyName":
            print(subchild.tag, subchild.text)
            myString+= ("The " + subchild.tag + " is " + subchild.text + "\n")
        elif subchild.tag == "PostDate":  
            print(subchild.tag, subchild.text)
            myString+= ("The " + subchild.tag + " is " + subchild.text + "\n")
        elif subchild.tag == "CloseDate":
            print(subchild.tag, subchild.text)
            myString+= ("The " + subchild.tag + " is " + subchild.text + "\n")
        elif subchild.tag == "LastUpdatedDate":
            print(subchild.tag, subchild.text)
            myString+= ("The " + subchild.tag + " is " + subchild.text + "\n")
        elif subchild.tag == "AwardCeiling":
            print(subchild.tag, subchild.text)
            myString+= ("The " + subchild.tag + " is " + subchild.text + "\n")
        elif subchild.tag == "AwardFloor":
            print(subchild.tag, subchild.text)
            myString+= ("The " + subchild.tag + " is " + subchild.text + "\n")        
        elif subchild.tag == "EstimatedTotalProgramFunding":
            print(subchild.tag, subchild.text)
            myString+= ("The " + subchild.tag + " is " + subchild.text + "\n")
        elif subchild.tag == "ExpectedNumberOfAwards":
            print(subchild.tag, subchild.text)
            myString+= ("The " + subchild.tag + " is " + subchild.text + "\n")
        elif subchild.tag == "Description":
            print(subchild.tag, subchild.text)
            myString+= ("The " + subchild.tag + " is " + subchild.text + "\n")
        elif subchild.tag == "Version":
            print(subchild.tag, subchild.text)
            myString+= ("The " + subchild.tag + " is " + subchild.text + "\n")
        elif subchild.tag == "CostSharingOrMatchingRequirement":
            print(subchild.tag, subchild.text)
            myString+= ("The " + subchild.tag + " is " + subchild.text + "\n")
        elif subchild.tag == "ArchiveDate":
            print(subchild.tag, subchild.text)
            myString+= ("The " + subchild.tag + " is " + subchild.text + "\n")
        elif subchild.tag == "GrantorContactEmail":
            print(subchild.tag, subchild.text)
            myString+= ("The " + subchild.tag + " is " + subchild.text + "\n")        
        elif subchild.tag == "GrantorContactEmailDescription":
            print(subchild.tag, subchild.text)
            myString+= ("The " + subchild.tag + " is " + subchild.text + "\n")
        elif subchild.tag == "GrantorContactText":
            print(subchild.tag, subchild.text)
            myString+= ("The " + subchild.tag + " is " + subchild.text + "\n")
    mySet.add(myString)
