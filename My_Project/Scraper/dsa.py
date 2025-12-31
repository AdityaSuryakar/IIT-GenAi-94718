from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def scrape_dsa(url="https://sunbeaminfo.in/modular-courses/data-structure-algorithms-using-java",
               output_file="dsa.txt"):
    """
    Scrapes the Sunbeam DSA course page and writes details to a text file.

    Parameters:
    - url: str, the URL of the DSA course page
    - output_file: str, file path to save the scraped content
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

            plus_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='#collapseFive']")))
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

            file.write("\n========== COURSE CONTENT ==========\n")

            # ================= COURSE CONTENT =================
            accordion_links = [
                "//a[@href='#collapse218']",
                "//a[@href='#collapse131']",
                "//a[@href='#collapse125']",
                "//a[@href='#collapse124']",
                "//a[@href='#collapse126']",
                "//a[@href='#collapse123']",
                "//a[@href='#collapse122']"
            ]

            for xpath in accordion_links:
                try:
                    button = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
                    section_title = button.text.strip() or "Course Section"

                    driver.execute_script("arguments[0].scrollIntoView(true);", button)
                    button.click()

                    target_id = button.get_attribute("href").split("#")[-1]
                    content = wait.until(EC.visibility_of_element_located((By.ID, target_id)))
                    time.sleep(0.5)

                    file.write(f"\n===== {section_title.upper()} =====\n")
                    file.write(content.text + "\n")

                except Exception:
                    continue

    finally:
        driver.quit()

    print(f"✅ Scraping completed → {output_file}")


if __name__ == "__main__":
    scrape_dsa()
