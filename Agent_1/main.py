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
def generate_queries(variation, brand_settings):
    brand_names = brand_settings.get("names", [])
    brand_names.append("")
    queries = []
    for brand_name in brand_names:
        query = f"\"{variation}\" {brand_name}"
        if brand_name == "":
            query = f"\"{variation}\""
        query = f"https://www.google.com/search?q={query}"
        queries.append(query)
    return queries
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


#Variation is passed in
if __name__=="__main__":
    current_directory = os.getcwd()
    settings_directory = os.path.join(current_directory, "brand_settings.json")
    settings = json.loads(open(settings_directory).read())
    brand_settings = BrandSettings(settings)
    test_settings = brand_settings.get_rules_for_brand("Givenchy")
    final_output=[]
    variation="BB50V9B1UC105"#Temp valueneeds to be passed in
    queries = generate_queries(variation,test_settings)
    for query in queries:
        driver=webdriver.Chrome(options=options)
        driver.get(query)
        page_source = driver.execute_script("return document.documentElement.outerHTML;")
        output_urls=parse_google_results(page_source)
        single_output={"Variation":variation,"Search Query": query.split("search?q=")[1],"Unfiltered URLs":output_urls}
        final_output.append(single_output)
    print(final_output)