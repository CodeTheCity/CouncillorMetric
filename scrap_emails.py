import csv
import re

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
            list_of_rows.append(row)
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

for link in links:
    se_driver.get(link)
    # get committees
    div = se_driver.find_element(By.CLASS_NAME, "mgUserBody")
    href = []
    ul= div.find_element(By.CLASS_NAME, "mgBulletList").find_elements(By.TAG_NAME, "li").find_element(By.TAG_NAME, "a").get_attribute("href")

Content = se_driver.find_element(By.ID, "modgov").find_element(By.CLASS_NAME, "mgContent").text.strip("\n")

# Extracting the email addresses
emails = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", Content)
print(emails)