from libraries.common import log_message, capture_page_screenshot, act_on_element, files, file_system, check_file_download_complete, pdf
from config import OUTPUT_FOLDER
import random, os, time
from selenium.webdriver.common.keys import Keys

class Searchpe():

    def __init__(self, rpa_selenium_instance, credentials:dict):
        self.browser = rpa_selenium_instance
        self.searchpe_url = credentials["url"]
        self.results_data = []

    def access_searchpe(self):
        """
        Access gob.pe/busqueda from the browser
        """
        log_message("Start - Access Peru's Search")
        self.browser.go_to(self.searchpe_url)
        log_message("End - Access Peru's Search")

    def initial_search(self):
        """
        Search in the page with a Keyword given
        """
        log_message("Start - Initial Search")
        
        search_term = os.environ.get("Search", "Peru")
        search_bar = act_on_element('//input[@placeholder="Buscar en Gob.pe"]', "find_element")
        self.browser.input_text_when_element_is_visible('//input[@placeholder="Buscar en Gob.pe"]', search_term)
        search_bar.send_keys(Keys.ENTER) 
        act_on_element('//h2[@class="text-2xl"]', "find_element")
        
        log_message("End - Initial Search")

    def filter_page(self):
        """
        Set the filters for the search
        """
        log_message("Start - Set the Filters")

        first_date = os.environ.get("Start", "01-01-2022")
        end_date = os.environ.get("End", "01-03-2022")     

        url =self.browser.get_location()
        search_filters= url.split("?")
        #https://www.gob.pe/busquedas?sheet=1&sort_by=none&term=Peru
        while len(search_filters) < 2:
            url =self.browser.get_location()
            search_filters= url.split("?")
            time.sleep(1)

        new_filters = "desde={}&hasta={}&".format(first_date, end_date)+search_filters[1]
        new_url = search_filters[0]+"?"+new_filters
        self.browser.go_to(new_url)
        act_on_element('//label[text()="Informes y publicaciones"]/span', "click_element")
        url =self.browser.get_location()
        search_filters= url.split("]")
        #https://www.gob.pe/busquedas?contenido[]=publicaciones&sheet=1&sort_by=none&term=Peru
        while len(search_filters) < 2:
            url =self.browser.get_location()
            search_filters= url.split("]")
            time.sleep(1)

        log_message("End - Set the Filters")

    def find_articles(self):
        """
        Find the first five articles with a Download Button
        """
        log_message("Start - Find the Articles")
        
        articles_list = act_on_element('//article[descendant::a[text()="Descargar"]]', "find_elements")
        download_list = act_on_element('//article//a[text()="Descargar"]', "find_elements")

        #print(len(download_list))

        article_data_list = []

        for article, download_link in zip(articles_list[::5], download_list[::5]):
            title = article.text.split("\n")[2]
            description = article.text.split("\n")[4]
            act_on_element(download_link, "click_element")
            check_file_download_complete("pdf")
            file_name = download_link.get_attribute("href").split("/")[-1]
            
            article_data_list.append({"Title": title, "Description": description, "Filename": file_name})

        self.article_data_list = article_data_list
        log_message("End - Find the Articles")

    def create_excel(self):
        """
        Create the Excel file with the information
        """
        log_message("Start - Create Excel")
        files.create_workbook(path = "{}/Files.xlsx".format(OUTPUT_FOLDER))
        files.create_worksheet(name = "Results", content= None, exist_ok = True, header = False)
        files.append_rows_to_worksheet(self.article_data_list, name = "Results", header = True, start= None)
        files.remove_worksheet(name = "Sheet")
        files.save_workbook(path = None)
        files.close_workbook()
        log_message("End - Create Excel")