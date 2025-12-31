from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def scrape_apache_details(url, output_file):
    """
    Scrapes course details from a Sunbeam course page and writes to a text file.
    
    Parameters:
    - url: str, URL of the course page
    - output_file: str, path to save the scraped content
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 20)

    try:
        driver.get(url)

        with open(output_file, "w", encoding="utf-8") as file:

            # ================= COURSE CATEGORY =================
            file.write("========== COURSE CATEGORY ==========\n")
            course_cat = wait.until(EC.presence_of_element_located((By.ID, "course_cat")))
            file.write(course_cat.text + "\n\n")

            # ================= BATCH DETAILS =================
            file.write("========== BATCH DETAILS ==========\n")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            plus_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//a[@href='#collapseFive']"))
            )
            plus_button.click()

            table = wait.until(EC.presence_of_element_located((By.ID, "collapseFive")))
            tbody = table.find_element(By.TAG_NAME, "tbody")
            rows = tbody.find_elements(By.TAG_NAME, "tr")

            for row in rows:
                cols = row.find_elements(By.TAG_NAME, "td")
                if len(cols) >= 5:
                    file.write(
                        f"Sr.No: {cols[0].text}\n"
                        f"Batch Code: {cols[1].text}\n"
                        f"Start Date: {cols[2].text}\n"
                        f"End Date: {cols[3].text}\n"
                        f"Time: {cols[4].text}\n"
                        "------------------------------\n"
                    )

            file.write("\n")

            # ================= COURSE CONTENT =================
            sections = [
                ("Target Audience", "collapse309"),
                ("Syllabus", "collapse310"),
                ("Prerequisite", "collapse311"),
                ("Tools & Setup", "collapse312"),
                ("Outcome", "collapse313"),
                ("Important Notes", "collapse314")
            ]

            file.write("========== COURSE CONTENT ==========\n")

            for title, cid in sections:
                try:
                    button = wait.until(
                        EC.element_to_be_clickable((By.XPATH, f"//a[@href='#{cid}']"))
                    )
                    driver.execute_script("arguments[0].scrollIntoView(true);", button)
                    button.click()

                    content = wait.until(EC.visibility_of_element_located((By.ID, cid)))
                    time.sleep(0.5)

                    file.write(f"\n===== {title.upper()} =====\n")
                    file.write(content.text + "\n")

                except Exception:
                    file.write(f"\n===== {title.upper()} =====\n")
                    file.write("Content not available.\n")

    finally:
        driver.quit()

    print(f"✅ Scraping completed successfully → {output_file}")


if __name__ == "__main__":
    URL = "https://www.sunbeaminfo.in/modular-courses/apache-spark-mastery-data-engineering-pyspark"
    OUTPUT_FILE = "apache.txt"
    scrape_apache_details(URL, OUTPUT_FILE)
