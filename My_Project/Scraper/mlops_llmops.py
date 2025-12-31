from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def llmops_mlops(url, output_file="mlops_llmops.txt"):
    """
    Scrapes Sunbeam MLOps/LLMOps course page and writes details to a text file.

    Parameters:
    - url: str, the URL of the MLOps/LLMOps course page
    - output_file: str, file path to save the scraped content
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 20)

    try:
        driver.get(url)

        with open(output_file, "w", encoding="utf-8") as f:

            # ================= COURSE OVERVIEW =================
            f.write("===== COURSE OVERVIEW =====\n\n")
            course_cat = wait.until(EC.presence_of_element_located((By.ID, "course_cat")))
            f.write(course_cat.text + "\n\n")

            # ================= COURSE DETAILS =================
            f.write("===== COURSE DETAILS =====\n\n")
            collapse_links = [
                "//a[@href='#collapse317']",
                "//a[@href='#collapse318']"
            ]

            for xpath in collapse_links:
                try:
                    button = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
                    driver.execute_script("arguments[0].scrollIntoView(true);", button)
                    button.click()

                    collapse_id = button.get_attribute("href").split("#")[-1]
                    content = wait.until(EC.visibility_of_element_located((By.ID, collapse_id)))
                    driver.execute_script("arguments[0].scrollIntoView(true);", content)
                    time.sleep(0.5)

                    # ❌ Do NOT write collapse IDs
                    f.write(content.text + "\n\n")
                    f.write("-" * 60 + "\n\n")
                except Exception:
                    continue

            # ================= BATCH SCHEDULE =================
            f.write("===== BATCH SCHEDULE =====\n\n")

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
                if len(cols) < 5:
                    continue

                f.write(
                    f"Sr.No      : {cols[0].text}\n"
                    f"Batch Code : {cols[1].text}\n"
                    f"Start Date : {cols[2].text}\n"
                    f"End Date   : {cols[3].text}\n"
                    f"Time       : {cols[4].text}\n"
                    + "-" * 40 + "\n"
                )

    finally:
        driver.quit()

    print(f"✅ Scraping completed → {output_file}")


if __name__ == "__main__":
    URL = "https://sunbeaminfo.in/modular-courses/mlops-llmops-training-institute-pune"
    llmops_mlops(URL)
