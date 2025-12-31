from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def internship_details(url="https://sunbeaminfo.in/internship",
                       output_file="internship_details.txt"):
    """
    Scrapes Sunbeam internship page and writes details to a text file.

    Parameters:
    - url: str, the URL of the internship page
    - output_file: str, file path to save the scraped content
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 20)

    try:
        driver.get(url)

        with open(output_file, "w", encoding="utf-8") as file:

            # ================= INTERNSHIP OVERVIEW =================
            file.write("===== INTERNSHIP OVERVIEW =====\n")
            content = wait.until(EC.presence_of_element_located((By.ID, "internship")))
            file.write(content.text + "\n\n")

            # ================= STUDENT INDUSTRIAL TRAINING & INTERNSHIP =================
            file.write("===== STUDENT INDUSTRIAL TRAINING & INTERNSHIP =====\n")
            button = wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Student Industrial Training & Internship"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", button)
            button.click()

            table_section = wait.until(EC.presence_of_element_located((By.ID, "collapseOneA")))
            table = table_section.find_element(By.TAG_NAME, "table")
            tbody = table.find_element(By.TAG_NAME, "tbody")
            rows = tbody.find_elements(By.TAG_NAME, "tr")

            for row in rows:
                cols = row.find_elements(By.TAG_NAME, "td")
                if len(cols) < 4:
                    continue
                file.write(f"Sr No      : {cols[0].text}\n")
                file.write(f"Duration   : {cols[1].text}\n")
                file.write(f"Structure  : {cols[2].text}\n")
                file.write(f"Mode       : {cols[3].text}\n")
                file.write("-" * 40 + "\n")

            file.write("\n")

            # ================= INDUSTRIAL PROGRAM =================
            file.write("===== INDUSTRIAL PROGRAM =====\n")
            button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='#collapseTwo']")))
            driver.execute_script("arguments[0].scrollIntoView(true);", button)
            button.click()

            content = wait.until(EC.visibility_of_element_located((By.ID, "collapseTwo")))
            time.sleep(1)
            file.write(content.text + "\n\n")

            # ================= PROGRAM BENEFITS =================
            file.write("===== PROGRAM BENEFITS =====\n")
            button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='#collapseFour']")))
            driver.execute_script("arguments[0].scrollIntoView(true);", button)
            button.click()

            content = wait.until(EC.visibility_of_element_located((By.ID, "collapseFour")))
            time.sleep(1)
            file.write(content.text + "\n\n")

    finally:
        driver.quit()

    print(f"✅ Internship data saved → {output_file}")


if __name__ == "__main__":
    internship_details()
