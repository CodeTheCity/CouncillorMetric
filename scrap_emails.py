import csv
import re
import json

from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def csv_maker(filename: str, fields: list, rows: list) -> None:
    """Write the contents to a CSV file with the given name."""
    with Path(filename).open("w") as csv_maker:
        csv_file_maker = csv.DictWriter(csv_maker, fields, delimiter=",")
        csv_file_maker.writeheader()  # writes the header
        """creates the rows"""
        for row in rows:
            csv_file_maker.writerow(row)

def csv_reader(filename: str, fields: list) -> list[str]:
    """Print to terminal the contents of csv file."""
    with Path(filename).open() as csv_reader:
        csv_file_reader = csv.DictReader(csv_reader, fields, delimiter=",")
        next(csv_file_reader)
        list_of_rows = []
        for row in csv_file_reader:
            list_of_rows.append(row) # modified to return the list of rows
            print(row)
        return list_of_rows

URL = "https://committees.aberdeencity.gov.uk/mgMemberIndex.aspx?bcr=1"

Opts = Options()
Opts.add_argument("--headless=new")
Opts.add_argument("--disable-extensions")

se_driver = webdriver.Chrome(options=Opts)
se_driver.get(URL)
se_driver.implicitly_wait(10)
concilors = se_driver.find_element(By.CLASS_NAME, "mgThumbsList")
concilors_link = concilors.find_elements(By.TAG_NAME, "a")

# Store all the links in a list
links = [c.get_attribute("href") for c in concilors_link]

committees = dict()
for i in range(len(links)):
    se_driver.get(links[i])
    councillor_name = se_driver.find_element(By.ID, "modgov").find_element(By.TAG_NAME, "h1").text.strip()
    print(councillor_name)
    committees[councillor_name] = []
    # get committees
    ul= se_driver.find_element(By.XPATH, "/html/body/div[2]/div[4]/div[3]/div[2]/div[2]/div[3]/ul[1]").find_elements(By.TAG_NAME, "li")
    for x in ul:
        committees[councillor_name].append(x.find_element(By.TAG_NAME, "a").get_attribute("href"))

committee_members = dict()
for councillor in committees:
    for href in committees[councillor]:
        print(href)
        se_driver.get(href)
        ul = se_driver.find_element(By.XPATH, "/html/body/div[2]/div[4]/div[3]/div[2]/div[2]/ul/li[2]").find_element(By.TAG_NAME, "a").get_attribute("href")
        se_driver.get(ul)
        ul = se_driver.find_element(By.XPATH, "/html/body/div[2]/div[4]/div[3]/div[2]/div[2]/ul/li").find_element(By.TAG_NAME, "a").get_attribute("href")
        se_driver.get(ul)
        # get commitee name
        committee_title = se_driver.find_element(By.XPATH, "/html/body/div[2]/div[4]/div[3]/div[2]/div[1]/h2").text
        # get emails
        Content = se_driver.find_element(By.XPATH, "/html/body/div[2]/div[4]/div[3]/div[2]/div[5]").find_element(By.TAG_NAME, "p").text
        print(Content)
        # Extracting the email addresses
        emails = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", Content)
        print(emails)
        committee_members[committee_title] = emails

print(committee_members)
se_driver.quit()


with open("sample.json", "w") as outfile: 
    json.dump(committee_members, outfile)