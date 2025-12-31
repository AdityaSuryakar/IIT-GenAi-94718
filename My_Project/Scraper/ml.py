from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def ml(url, output_file="ml.txt"):
    """
    Scrapes Sunbeam Machine Learning course page and writes details to a text file.

    Parameters:
    - url: str, the URL of the Machine Learning course page
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
                "//a[@href='#collapse266']",
                "//a[@href='#collapse194']",
                "//a[@href='#collapse193']",
                "//a[@href='#collapse192']",
                "//a[@href='#collapse191']",
                "//a[@href='#collapse190']",
                "//a[@href='#collapse189']"
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

                    f.write(content.text + "\n\n")
                    f.write("-" * 60 + "\n\n")
                except Exception:
                    continue

    finally:
        driver.quit()

    print(f"✅ Scraping completed → {output_file}")


if __name__ == "__main__":
    URL = "https://sunbeaminfo.in/modular-courses/machine-learning-classes"
    ml(URL)
