from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def scrape_sunbeam_about_us(output_file="about_us.txt"):
    """
    Scrapes Sunbeam Info About Us and branch details and saves into a text file.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 25)

    try:
        with open(output_file, "w", encoding="utf-8") as file:

            # Visit main About Us page
            driver.get("https://sunbeaminfo.in/about-us")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            file.write("===== ABOUT US =====\n\n")

            main_div = wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, ".main_info.wow.fadeInUp")
                )
            )

            # Extract paragraphs from main section
            paragraphs = main_div.find_elements(By.TAG_NAME, "p")
            for p in paragraphs:
                text = p.text.strip()
                if text:
                    file.write(text + "\n\n")

            # Expand "About Sunbeam" section
            expand_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//a[@href='#collapse4']"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", expand_button)
            driver.execute_script("arguments[0].click();", expand_button)

            branch_section = wait.until(
                EC.visibility_of_element_located((By.ID, "collapse4"))
            )
            time.sleep(1)

            file.write("===== ABOUT SUNBEAM =====\n\n")

            # Click again to make sure content is visible
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", expand_button)
            driver.execute_script("arguments[0].click();", expand_button)

            content_div = wait.until(
                EC.visibility_of_element_located((By.ID, "collapse4"))
            )
            time.sleep(1)

            paragraphs = content_div.find_elements(By.TAG_NAME, "p")
            for p in paragraphs:
                text = p.text.strip()
                if text:
                    file.write(text + "\n\n")

            file.write("===== BRANCHES =====\n\n")
            file.write(branch_section.text.strip() + "\n\n")

            # Scrape Hinjawadi branch details
            driver.get("https://sunbeaminfo.in/branch/hinjawadi")
            hinjawadi_details = wait.until(
                EC.visibility_of_element_located((By.ID, "br_details"))
            )

            file.write("===== HINJAWADI BRANCH DETAILS =====\n\n")
            file.write(hinjawadi_details.text.strip() + "\n")

    finally:
        driver.quit()

    print(f"✔ All scraped data combined successfully into {output_file}")


if __name__ == "__main__":
    scrape_sunbeam_about_us()
