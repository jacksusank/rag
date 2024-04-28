# convert an xml file to a csv file

import csv

import lxml.etree as ET

# import xml.etree.ElementTree as ET
row_selector = r"{http://apply.grants.gov/system/OpportunityDetail-V1.0}OpportunitySynopsisDetail_1_0"
id_column = "OpportunityID"


def get_columns(root):
    columns = set()
    for member in root.iter(row_selector):
        for child in member.getchildren():
            columns.add(child.tag.split("}")[1])
    columns.remove(id_column)
    col_list = list(columns)
    col_list.sort()
    col_list = [id_column] + col_list
    return col_list


def xmltocsv(xmlfile, csvfile):
    tree = ET.parse(xmlfile, parser=ET.XMLParser(recover=True))
    root = tree.getroot()
    columns = get_columns(root)
    with open(csvfile, "w") as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(columns)
        for member in root.iter(row_selector):
            row = {}
            for col in member.getchildren():
                row[col.tag.split("}")[1]] = col.text.strip().replace("&lt;br/&gt", "")
            csvwriter.writerow([row.get(col, "") for col in columns])


if __name__ == "__main__":
    xmltocsv("test.xml", "data.csv")