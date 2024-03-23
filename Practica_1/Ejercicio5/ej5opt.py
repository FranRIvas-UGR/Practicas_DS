from bs4 import BeautifulSoup
import requests
from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.common.by import By
import os,sys
os.environ['MOZ_HEADLESS'] = '1'

class ScrapeStrategy():
    def scrape(self, url):
        pass
    
    def export_to_json(self, data, filename):
        pass


class BeautifulSoupStrategy(ScrapeStrategy):
    def _get_soup(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            return BeautifulSoup(response.content, 'html.parser')
        else:
            raise ValueError(f'Failed to retrieve the webpage, status code: {response.status_code}')
    
    def _find_elements(self, soup):
        open_value_td = soup.find('td', {'data-test': 'OPEN-value'})
        close_value_td = soup.find('td', {'data-test': 'PREV_CLOSE-value'})
        volume_value_td = soup.find('td', {'data-test': 'TD_VOLUME-value'})
        market_cap_value_td = soup.find('td', {'data-test': 'MARKET_CAP-value'})
        return open_value_td, close_value_td, volume_value_td, market_cap_value_td
    
    def _extract_values(self, open_value_td, close_value_td, volume_value_td, market_cap_value_td):
        open_value = open_value_td.text.strip() if open_value_td else 'Open Value not found'
        close_value = close_value_td.text.strip() if close_value_td else 'Close Value not found'
        volume = volume_value_td.text.strip() if volume_value_td else 'Volume Value not found'
        market_capitalization = market_cap_value_td.text.strip() if market_cap_value_td else 'Market Cap Value not found'
        return open_value, close_value, volume, market_capitalization
    
    def scrape(self, url):
        soup = self._get_soup(url)
        open_value_td, close_value_td, volume_value_td, market_cap_value_td = self._find_elements(soup)
        open_value, close_value, volume, market_capitalization = self._extract_values(open_value_td, close_value_td, volume_value_td, market_cap_value_td)
        return open_value, close_value, volume, market_capitalization
                
    def export_to_json(self, data, filename):
        # Data es una lista de open_value, close_value, volume, market_capitalization
        with open(filename, 'w') as file:
            file.write('{\n')
            file.write(f'  "Precio de apertura": "{data[0]}",\n')
            file.write(f'  "Precio de cierre anterior": "{data[1]}",\n')
            file.write(f'  "Volumen": "{data[2]}",\n')
            file.write(f'  "Capitalización de Mercado": "{data[3]}"\n')
            file.write('}\n')
        return filename


class SeleniumStrategy(ScrapeStrategy):
    class_reject_button = '//button[@class="btn secondary reject-all"]'
    class_open_value = '//td[@data-test="OPEN-value"]'
    class_close_value = '//td[@data-test="PREV_CLOSE-value"]'
    class_volume = '//td[@data-test="TD_VOLUME-value"]'
    class_market_capitalization = '//td[@data-test="MARKET_CAP-value"]'
    
    # Constructor de la clase (crea el driver)
    def __init__(self):
        self.options = FirefoxOptions()
        self.options.headless = True
        self.driver = Firefox(options=self.options)
    
    def __del__(self):
        self.driver.quit()
    
    def lanzarPagina(self, url):
        self.driver.get(url)
        return self.driver
        
    
    def rejectCookiesScrollDown(self, driver):  
        scroll_down_button = driver.find_element(By.XPATH, '//button[@id="scroll-down-btn"]')
        scroll_down_button.click()
        reject_button = driver.find_element(By.XPATH, self.class_reject_button)
        reject_button.click()
        return driver
    
    def getValues(self, driver):
        open_value_td = driver.find_element(By.XPATH, self.class_open_value)
        close_value_td = driver.find_element(By.XPATH, self.class_close_value)
        volume = driver.find_element(By.XPATH, self.class_volume)
        market_capitalization = driver.find_element(By.XPATH, self.class_market_capitalization)
        return open_value_td, close_value_td, volume, market_capitalization
    
    def stripValues(self, open_value_td, close_value_td, volume, market_capitalization):
        open_value = open_value_td.text.strip()
        close_value = close_value_td.text.strip()
        volume = volume.text.strip()
        market_capitalization = market_capitalization.text.strip()
        return open_value, close_value, volume, market_capitalization
    
    def export_to_json(self, data, filename):
        # Data es una lista de open_value, close_value, volume, market_capitalization
        with open(filename, 'w') as file:
            file.write('{\n')
            file.write(f'  "Precio de apertura": "{data[0]}",\n')
            file.write(f'  "Precio de cierre anterior": "{data[1]}",\n')
            file.write(f'  "Volumen": "{data[2]}",\n')
            file.write(f'  "Capitalización de Mercado": "{data[3]}"\n')
            file.write('}\n')
    
    def scrape(self, url):
        driver = self.lanzarPagina(url)
        driver = self.rejectCookiesScrollDown(driver)
        open_value_td, close_value_td, volume, market_capitalization = self.getValues(driver)
        open_value, close_value, volume, market_capitalization = self.stripValues(open_value_td, close_value_td, volume, market_capitalization)
        data = open_value, close_value, volume, market_capitalization
        return data
    

class Context:
    def __init__(self, strategy):
        self._strategy = strategy

    def set_strategy(self, strategy):
        self._strategy = strategy

    def scrape(self, url):
        return self._strategy.scrape(url)



url = 'https://finance.yahoo.com/quote/TSLA'

context = Context(SeleniumStrategy())
context2 = Context(BeautifulSoupStrategy())

open_value, close_value, volume, market_capitalization = context.scrape(url)
open_value2, close_value2, volume2, market_capitalization2 = context2.scrape(url)

data = [open_value, close_value, volume, market_capitalization]
data2 = [open_value2, close_value2, volume2, market_capitalization2]

filename = sys.argv[1]
filename2 = sys.argv[2]

context._strategy.export_to_json(data, filename)
context2._strategy.export_to_json(data2, filename2)

print(f'Exporto a {filename}')
print(f'Exporto a {filename2}')
