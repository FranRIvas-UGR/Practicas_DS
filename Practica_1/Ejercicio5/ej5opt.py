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
    def scrape(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            open_value_td = soup.find('td', {'data-test': 'OPEN-value'})
            close_value_td = soup.find('td', {'data-test': 'PREV_CLOSE-value'})
            if open_value_td:
                return open_value_td.text.strip()
            else:
                return 'Open Value not found'
        else:
            return f'Failed to retrieve the webpage, status code: {response.status_code}'


class SeleniumStrategy(ScrapeStrategy):
    def scrape(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            options = FirefoxOptions()
            options.headless = True
            driver = Firefox(options=options)
            driver.get(url)
            
            final_scroll_button = driver.find_element(By.XPATH, '//button[@id="scroll-down-btn"]')
            final_scroll_button.click()
            
            reject_button = driver.find_element(By.XPATH, '//button[@class="btn secondary reject-all"]')
            reject_button.click()
            
            open_value_td = driver.find_element(By.XPATH, '//td[@data-test="OPEN-value"]')
            close_value_td = driver.find_element(By.XPATH, '//td[@data-test="PREV_CLOSE-value"]')
            volume = driver.find_element(By.XPATH, '//td[@data-test="TD_VOLUME-value"]')
            market_capitalization = driver.find_element(By.XPATH, '//td[@data-test="MARKET_CAP-value"]')
            
            if not open_value_td:
                return 'Precio de apertura no encontrado' 
            if not close_value_td:
                return 'Precio de cierre anterior no encontrado'
            if not volume:
                return 'Volumen no encontrado'
            if not market_capitalization:
                return 'Capitalización de Mercado no encontrada'
            
            open_value = open_value_td.text.strip()
            close_value = close_value_td.text.strip()
            volume = volume.text.strip()
            market_capitalization = market_capitalization.text.strip()
            driver.quit()
            return open_value, close_value, volume, market_capitalization
        else:
            return f'Failed to retrieve the webpage, status code: {response.status_code}'
        
        
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
    

class Context:
    def __init__(self, strategy):
        self._strategy = strategy

    def set_strategy(self, strategy):
        self._strategy = strategy

    def scrape(self, url):
        return self._strategy.scrape(url)



url = 'https://finance.yahoo.com/quote/TSLA'
context = Context(SeleniumStrategy())
open_value, close_value, volume, market_capitalization = context.scrape(url)

data = [open_value, close_value, volume, market_capitalization]
filename = sys.argv[1]
context._strategy.export_to_json(data, filename)
print(f'Exporto a {filename}')
