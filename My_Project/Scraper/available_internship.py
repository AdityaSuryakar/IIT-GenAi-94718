from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def available_internship(output_file="available_internships.txt", headless=True):
    """
    Scrapes internship information and batches from Sunbeam website
    and saves it to a text file.

    Parameters:
    - output_file: str, path to save scraped data
    - headless: bool, whether to run Chrome in headless mode
    """
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 10)

    try:
        driver.get("https://sunbeaminfo.in/internship")
        driver.implicitly_wait(5)

        # Load dynamic content
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        plus_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[@href='#collapseSix']"))
        )
        plus_button.click()

        table = driver.find_element(By.ID, "collapseSix")
        tbody = table.find_element(By.TAG_NAME, "tbody")
        rows = tbody.find_elements(By.TAG_NAME, "tr")

        # Extract data and save
        with open(output_file, "w", encoding="utf-8") as file:
            for row in rows:
                cols = row.find_elements(By.TAG_NAME, "td")
                if len(cols) < 5:
                    continue

                info = {
                    "technology": cols[0].text,
                    "aim": cols[1].text,
                    "prerequisite": cols[2].text,
                    "learning": cols[3].text,
                    "location": cols[4].text
                }

                for key, value in info.items():
                    file.write(f"{key}: {value}\n")
                file.write("-" * 40 + "\n")

    finally:
        driver.quit()

    print(f"✅ Internship data scraped successfully → {output_file}")


if __name__ == "__main__":
    available_internship()
