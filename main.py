import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import html2text

urls = [
    "https://qavanin.ir/Law/TreeText/?IDS=14010540403702484380",
    "https://qavanin.ir/Law/TreeText/?IDS=996330350596472987",
    "https://qavanin.ir/Law/TreeText/?IDS=11626740677693601128",
    "https://qavanin.ir/Law/TreeText/?IDS=10400207744629756269",
    "https://qavanin.ir/Law/TreeText/?IDS=1560535278057796779",
]





class Task():

    def prepare_driver(self) -> WebDriver:

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        chrome_options.add_argument(f"user-agent={user_agent}")
        
        driver = webdriver.Chrome(options=chrome_options)
        return driver


    def fetch_data(self, url):

        try:
            driver = self.prepare_driver()
            driver.get(url)
            time.sleep(3)

            main_content = driver.find_element(by=By.ID, value='treeText').get_attribute('innerHTML')
            return main_content

        except Exception:
            pass

        finally:
            driver.close()


    def convert_to_markdown(self, text) -> str:

        return html2text.html2text(text)


    def save_markdown(self, content, path):

        with open(path, 'w', encoding='utf-8') as file:
            file.write(content)


for i, url in enumerate(urls):
    try:
        task = Task()

        text = task.fetch_data(url)
        md_content = task.convert_to_markdown(text)

        output_dir = "markdown"
        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, f"page_{i+1}.md")

        task.save_markdown(md_content, file_path)

    except Exception as exc:
        print(exc)
