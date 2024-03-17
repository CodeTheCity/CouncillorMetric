import csv

from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

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
councillors = []
for link in links:
    
    se_driver.get(link)
    councillor_name = se_driver.find_element(By.ID, "modgov").find_element(By.TAG_NAME, "h1").text.strip().strip().strip('"')
    councillor_img = se_driver.find_element(By.ID,"modgov").find_element(By.CLASS_NAME, "mgBigPhoto").find_element(By.TAG_NAME, "img").get_attribute("src")
    councillor_party_ward = se_driver.find_element(By.CLASS_NAME, "mgUserSideBar").find_elements(By.TAG_NAME, "p")
    councillor_party = councillor_party_ward[0].text
    councillor_ward = councillor_party_ward[1].text
    attendance_page = se_driver.find_element(By.CLASS_NAME, "mgBulletList").find_element(By.TAG_NAME, "a").get_attribute("href")

    # attendance page
    se_driver.get(attendance_page)
    date_range = se_driver.find_element(By.ID, "DateRange").get_attribute("value")
    table = se_driver.find_element(By.ID, "mgattendbreakdown")
    t = table.text.split("\n")

    if len(t) == 6:
        expected = t[2].split(":")[1].strip() 
        present = t[3].split(":")[1].split("  ")[0].strip()
        present_percent = t[3].split(":")[1].split("  ")[1].strip()
        apologies = t[4].split(":")[1].split("  ")[0].strip()
        apologies_percent = t[4].split(":")[1].split("  ")[1].split(" ")[1]
        absent = t[5].split(":")[1].split("  ")[0].strip()
        absent_percent = t[5].split(":")[1].split("  ")[1].strip()
        
    if len(t) == 5:
        expected = t[2].split(":")[1].strip() 
        present = t[3].split(":")[1].split("  ")[0].strip()
        present_percent = t[3].split(":")[1].split("  ")[1].strip()
        apologies = t[4].split(":")[1].split("  ")[0].strip()
        apologies_percent = t[4].split(":")[1].split("  ")[1].split(" ")[1]
        absent = "0"
        absent_percent = "0%"

    councillor = {"Name": councillor_name,"Image":councillor_img,
                "Party":councillor_party, "Ward": councillor_ward, 
                "Date":date_range,
                   "Expected": expected, "Present": present, "Present Percent": present_percent,
                     "Apologies": apologies, "Apologies Percent": apologies_percent,"Absent": absent,
                       "Absent Percent": absent_percent}
    councillors.append(councillor)
    se_driver.execute_script("window.history.go(-2)")  # Go back to the original page

se_driver.quit()  # Close the driver when done

def csv_maker(filename: str, fields: list, rows: list) -> None:
    """Write the contents to a CSV file with the given name."""
    with Path(filename).open("w") as csv_maker:
        csv_file_maker = csv.DictWriter(csv_maker, fields, delimiter=",")
        csv_file_maker.writeheader()  # writes the header
        """creates the rows"""
        for row in rows:
            csv_file_maker.writerow(row)

fields = ["Name","Image",
           "Party", "Ward",
           "Date","Expected", 
          "Present","Present Percent", "Apologies",
             "Apologies Percent", "Absent", "Absent Percent"]
csv_maker("councillorsAttendance.csv", fields, councillors)