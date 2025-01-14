import json
import os

from bs4 import BeautifulSoup
from selenium import webdriver
options = webdriver.ChromeOptions()
options.add_argument("--auto-open-devtools-for-tabs")
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
options.add_argument("--start-maximized")
options.add_argument("--incognito")
options.add_argument("--enable-javascript")
options.add_argument('--no-sandbox')
options.add_argument('--disable-setuid-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--headless=new")
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")

def parse_google_results(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    results = []
    for g in soup.find_all('div', class_='g'):
        links = g.find_all('a')
        if links and 'href' in links[0].attrs:  # check if 'href' attribute exists
            results.append(links[0]['href'])
    return results
class BrandSettings:
    def __init__(self, settings):
        self.settings = settings

    def get_rules_for_brand(self, brand_name):
        for rule in self.settings['brand_rules']:
            if str(brand_name).lower() in str(rule['names']).lower():
                return rule
        return None


#Query, Variation are passed in
if __name__=="__main__":
    current_directory = os.getcwd()
    settings_directory = os.path.join(current_directory, "brand_settings.json")
    settings = json.loads(open(settings_directory).read())
    brand_settings = BrandSettings(settings)
    test_settings = brand_settings.get_rules_for_brand("Givenchy") #Temp value needs to be passed in
    driver=webdriver.Chrome(options=options)
    query='https://www.google.com/search?q="BB50V9B1UC105" GIV' #Passed in by manager
    variation="BB50V9B1UC105 GIV" #Passed in
    driver.get(query)
    page_source = driver.execute_script("return document.documentElement.outerHTML;")
    output_urls=parse_google_results(page_source)
    output={"Variation":variation,"Search Query": query.split("search?q=")[1],"Unfiltered URLs":output_urls}
    print(output)