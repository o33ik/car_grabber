import bs4
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def presence_of_either_element(driver, css_selector1, css_selector2):
    def condition(driver):
        try:
            return EC.presence_of_element_located((By.CSS_SELECTOR, css_selector1))(driver)
        except:
            return EC.presence_of_element_located((By.CSS_SELECTOR, css_selector2))(driver)
    return condition

class BidfaxGrabber:
    def grab(self, vin):
        if self.valid_vin(vin):
            options = webdriver.ChromeOptions()
            options.binary_location = r"C:/Program Files/Google/Chrome/Application/chrome.exe"
            chrome_driver_binary = r"D:/work/car_grabber/backend/chromedriver.exe"
            driver = webdriver.Chrome(chrome_driver_binary, chrome_options=options)
            url = f'https://bid.cars/en/search/results?search-type=typing&query={vin}'
            try:
                driver.get(url)
                custom_condition = presence_of_either_element(driver, "div.nothing-found", "span.vin-drop")
                element = WebDriverWait(driver, 5).until(custom_condition)
                soup = bs4.BeautifulSoup(driver.page_source, 'lxml')

                if (element.get_attribute("class") == 'nothing-found'):
                    return {
                        'requested_url': url,
                        'result': 'nothing found',
                        'image_urls': []
                    }
                else:
                    return {
                        'requested_url': url,
                        'result': 'something found',
                        'image_urls': list(self.parse_result(soup))
                    }
            finally:
                driver.close()



        return None

    def valid_vin(self, vin):
        return not re.search(r'xxxx', vin)

    def parse_result(self, soup):
        images = soup.select('.f-carousel__slide img')
        return map(lambda i: i.attrs['src'], images)
