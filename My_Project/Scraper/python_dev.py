from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def python_dev(url="https://sunbeaminfo.in/modular-courses/python-classes-in-pune", 
               output_file="com22.txt"):
    """
    Scrapes Python course details (overview, content, batch schedule) from Sunbeam website
    and writes to a text file.

    Parameters:
    - url: str, URL of the Python course page
    - output_file: str, path to save the scraped content
    """
    # ---------------- Browser Setup ----------------
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 20)

    try:
        driver.get(url)

        with open(output_file, "w", encoding="utf-8") as file:

            # ==================================================
            # 1️⃣ COURSE OVERVIEW (course_cat)
            # ==================================================
            try:
                overview = wait.until(
                    EC.presence_of_element_located((By.ID, "course_cat"))
                )
                file.write("===== COURSE OVERVIEW =====\n")
                file.write(overview.text.strip() + "\n\n")
            except:
                pass

            # ==================================================
            # 2️⃣ ALL ACCORDION CONTENT (NO COLLAPSE IDS USED)
            # ==================================================
            file.write("===== COURSE CONTENT =====\n")

            accordion_buttons = driver.find_elements(
                By.XPATH, "//a[@data-toggle='collapse']"
            )

            seen_text = set()

            for btn in accordion_buttons:
                try:
                    driver.execute_script("arguments[0].scrollIntoView(true);", btn)
                    time.sleep(0.3)

                    if btn.get_attribute("aria-expanded") == "false":
                        btn.click()
                        time.sleep(0.7)

                    target_id = btn.get_attribute("href").split("#")[-1]
                    content = wait.until(
                        EC.visibility_of_element_located((By.ID, target_id))
                    )

                    text = content.text.strip()
                    if text and text not in seen_text:
                        file.write(text + "\n\n")
                        seen_text.add(text)

                except:
                    continue

            # ==================================================
            # 3️⃣ BATCH SCHEDULE TABLE
            # ==================================================
            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                schedule_btn = wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//a[contains(@href,'collapseFive')]")
                    )
                )
                schedule_btn.click()
                time.sleep(1)

                table = driver.find_element(By.ID, "collapseFive")
                rows = table.find_elements(By.TAG_NAME, "tr")

                file.write("===== BATCH SCHEDULE =====\n")

                for row in rows:
                    cols = row.find_elements(By.TAG_NAME, "td")
                    if len(cols) >= 5:
                        file.write(
                            f"Sr.No: {cols[0].text} | "
                            f"Batch Code: {cols[1].text} | "
                            f"Start Date: {cols[2].text} | "
                            f"End Date: {cols[3].text} | "
                            f"Time: {cols[4].text}\n"
                        )

                file.write("\n")

            except:
                pass

    finally:
        driver.quit()

    print(f"✅ Scraping completed successfully → {output_file}")


if __name__ == "__main__":
    python_dev()
