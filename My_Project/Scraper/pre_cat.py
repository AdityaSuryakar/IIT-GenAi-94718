from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def precat(output_file="precat.txt"):
    """
    Scrapes Sunbeam Pre-CAT and Modular Course content including tables and writes to a text file.

    Parameters:
    - output_file: str, file path to save the scraped content
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 20)

    def scrape_table_by_id(collapse_id, min_cols):
        """
        Scrape a table by collapse ID.
        Returns a list of rows (each row is a list of column texts)
        """
        table_element = wait.until(EC.presence_of_element_located((By.ID, collapse_id)))
        rows = table_element.find_elements(By.TAG_NAME, "tr")
        data = []
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) < min_cols:
                continue
            data.append([c.text for c in cols])
        return data

    try:
        with open(output_file, "w", encoding="utf-8") as f:

            # 1️⃣ Modular Course – collapse302 (TEXT CONTENT)
            f.write("========== MODULAR COURSE : collapse302 ==========\n")
            driver.get("https://www.sunbeaminfo.in/modular-courses.php?mdid=57")
            btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='#collapse302']")))
            driver.execute_script("arguments[0].scrollIntoView(true);", btn)
            btn.click()
            content = wait.until(EC.presence_of_element_located((By.ID, "collapse302")))
            f.write(content.text + "\n\n")

            # 2️⃣ Pre-CAT – collapse1 (TEXT CONTENT)
            f.write("========== PRE-CAT : collapse1 ==========\n")
            driver.get("https://www.sunbeaminfo.in/pre-cat")
            btn1 = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='#collapse1']")))
            driver.execute_script("arguments[0].scrollIntoView(true);", btn1)
            btn1.click()
            content1 = wait.until(EC.presence_of_element_located((By.ID, "collapse1")))
            driver.execute_script("arguments[0].scrollIntoView(true);", content1)
            time.sleep(1)
            f.write(content1.text + "\n\n")

            # 3️⃣ Pre-CAT – collapse2 (TEXT CONTENT)
            f.write("========== PRE-CAT : collapse2 ==========\n")
            btn2 = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='#collapse2']")))
            driver.execute_script("arguments[0].scrollIntoView(true);", btn2)
            btn2.click()
            content2 = wait.until(EC.presence_of_element_located((By.ID, "collapse2")))
            f.write(content2.text + "\n\n")

            # 4️⃣ Pre-CAT – collapseThree (TABLE DATA)
            f.write("========== PRE-CAT TABLE : collapseThree ==========\n")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            btn3 = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='#collapseThree']")))
            driver.execute_script("arguments[0].scrollIntoView(true);", btn3)
            btn3.click()
            table_data = scrape_table_by_id("collapseThree", 7)
            for row in table_data:
                f.write(
                    f"Sr No: {row[0]}\nBatch Code: {row[1]}\nDuration: {row[2]}\n"
                    f"Start Date: {row[3]}\nEnd Date: {row[4]}\nTime: {row[5]}\nFees: {row[6]}\n"
                    "----------------------------------\n"
                )

            # 5️⃣ Modular Course – collapseFive (TABLE DATA)
            f.write("\n========== MODULAR COURSE TABLE : collapseFive ==========\n")
            driver.get("https://www.sunbeaminfo.in/modular-courses.php?mdid=57")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            btn5 = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='#collapseFive']")))
            driver.execute_script("arguments[0].scrollIntoView(true);", btn5)
            btn5.click()
            table_data = scrape_table_by_id("collapseFive", 5)
            for row in table_data:
                f.write(
                    f"Sr: {row[0]}\nBatch Code: {row[1]}\nStart Date: {row[2]}\n"
                    f"End Date: {row[3]}\nTime: {row[4]}\n"
                    "----------------------------------\n"
                )

    finally:
        driver.quit()

    print(f"✅ Data successfully scraped into {output_file}")


if __name__ == "__main__":
    precat()
