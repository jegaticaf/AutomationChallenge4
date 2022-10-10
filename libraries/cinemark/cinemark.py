from libraries.common import log_message, files, get_single_schedule
from config import OUTPUT_FOLDER, tabs_dict
import os, time
from selenium.webdriver.common.keys import Keys
from datetime import datetime, timedelta
import SeleniumLibrary.errors

class Cinemark():

    def __init__(self, rpa_selenium_instance, credentials:dict):
        self.browser = rpa_selenium_instance
        self.cinemark_url = credentials["url"]
        self.movie_information = []
        self.cinema_information = []
        self.movie_data_dict_list = []

    def access_cinemark(self):
        """
        Access the Cinemark page from the browser
        """
        log_message("Start - Access Cinemark.pe")
        self.browser.go_to(self.cinemark_url)
        try:
            self.browser.wait_until_element_is_visible('//select', timeout=timedelta(seconds=1))
            cinema_selection = self.browser.find_elements('//select')
            self.browser.click_element(cinema_selection[0])

            self.browser.click_element('//option[text()="Arequipa"]')
            self.browser.click_element(cinema_selection[1])

            self.browser.click_element('//option[text()="Cinemark Lambramani"]')        
            self.browser.click_element('//button[text()="Aceptar"]')
        except SeleniumLibrary.errors.ElementNotFound:
            log_message("Couldn't find the cinema pop-up")
        log_message("End - Access Cinemark.pe")

    def go_to_section(self, parameter:str):
        """
        Go to the section that is given as a parameter
        """
        log_message("Start - Go to section {}".format(parameter))
        self.browser.switch_window(locator = self.browser.get_window_handles()[tabs_dict["Cinemark"]])
        self.browser.go_to(self.cinemark_url)
        self.browser.click_element('//ul[@class="box-menu grid-center-content"]//a[text()="{}"]'.format(parameter))
        log_message("End - Go to section {}".format(parameter))

    def extract_movies_data(self):
        """
        Goes to each of the movies sections and takes all the information of each movie.
        """
        log_message("Start - Extract the movies information")
        try:
            self.browser.wait_until_element_is_visible('//button[text()="Cartelera"]', timeout=timedelta(seconds=1))
            self.browser.click_element('//button[text()="Cartelera"]')
            self.browser.wait_until_element_is_visible('//div[@class="movies-container row-margin-bottom col-lg-12"]/div[@class="movie-box-container"]', timeout=timedelta(seconds=3))
            current_movies = self.browser.find_elements('//div[@class="movies-container row-margin-bottom col-lg-12"]/div[@class="movie-box-container"]')
            self.browser.execute_javascript("window.open()")
            self.browser.switch_window(locator = "NEW")
            tabs_dict["Movie"] = len(tabs_dict)
            for movie in current_movies:
                self.browser.switch_window(locator = self.browser.get_window_handles()[tabs_dict["Cinemark"]])
                movie_link = self.browser.find_element('xpath:.//a', parent=movie).get_attribute("href")
                self.browser.switch_window(locator = self.browser.get_window_handles()[tabs_dict["Movie"]])
                self.browser.go_to(movie_link)
                self.browser.wait_until_element_is_visible('//div[@class="row movie-trailer-content"]//h1', timeout=timedelta(seconds=1))
                movie_title = self.browser.find_element('//div[@class="row movie-trailer-content"]//h1').text
                movie_data = self.browser.find_elements('//div[@class="movie-details"]//li')
                movie_rating = self.browser.find_element(movie_data[0]).text
                movie_duration = self.browser.find_element(movie_data[1]).text
                self.movie_information.append({"Title": movie_title, "Duration": movie_duration, "Rating": movie_rating})
            log_message("Finished the current movies")
            self.browser.switch_window(locator = self.browser.get_window_handles()[tabs_dict["Cinemark"]])
            self.browser.click_element('//button[text()="Preventa"]')
            presale_movies = self.browser.find_elements('//div[@id="sectionPreSale"]//div[@class="movie-box-container"]')
            for movie in presale_movies:
                self.browser.switch_window(locator = self.browser.get_window_handles()[tabs_dict["Cinemark"]])
                movie_link = self.browser.find_element('xpath:.//a', parent=movie).get_attribute("href")
                self.browser.switch_window(locator = self.browser.get_window_handles()[tabs_dict["Movie"]])
                self.browser.go_to(movie_link)
                self.browser.wait_until_element_is_visible('//div[@class="row movie-trailer-content"]//h1', timeout=timedelta(seconds=1))
                movie_title = self.browser.find_element('//div[@class="row movie-trailer-content"]//h1').text
                movie_data = self.browser.find_elements('//div[@class="movie-details"]//li')
                movie_rating = self.browser.find_element(movie_data[0]).text
                movie_duration = self.browser.find_element(movie_data[1]).text
                self.movie_information.append({"Title": movie_title, "Duration": movie_duration, "Rating": movie_rating})
            log_message("Finished the presale movies")
            self.browser.switch_window(locator = self.browser.get_window_handles()[tabs_dict["Cinemark"]])
            self.browser.click_element('//button[text()="Próximamente"]')
            soon_movies = self.browser.find_elements('//div[@id="sectionComingSoon"]//div[@class="movie-box-container"]')
            for movie in soon_movies:
                self.browser.switch_window(locator = self.browser.get_window_handles()[tabs_dict["Cinemark"]])
                movie_link = self.browser.find_element('xpath:.//a', parent=movie).get_attribute("href")
                self.browser.switch_window(locator = self.browser.get_window_handles()[tabs_dict["Movie"]])
                self.browser.go_to(movie_link)
                self.browser.wait_until_element_is_visible('//div[@class="row movie-trailer-content"]//h1', timeout=timedelta(seconds=1))
                movie_title = self.browser.find_element('//div[@class="row movie-trailer-content"]//h1').text
                movie_data = self.browser.find_elements('//div[@class="movie-details"]//li')
                movie_rating = self.browser.find_element(movie_data[0]).text
                movie_duration = self.browser.find_element(movie_data[1]).text
                self.movie_information.append({"Title": movie_title, "Duration": movie_duration, "Rating": movie_rating})
            log_message("Finished the coming soon movies")
        except SeleniumLibrary.errors.ElementNotFound:
            log_message("Had a problem getting the movie information")
        log_message("End - Extract the movies information")

    def extract_cinema_data(self):
        """
        Gets the information for every cinema
        """
        log_message("Start - Gets the cinema information")
        try:
            self.browser.wait_until_element_is_visible('//button[@class="more-theatres"]', timeout=timedelta(seconds=1))
            self.browser.click_element('//button[@class="more-theatres"]')
            self.browser.wait_until_element_is_visible('//div[@class="box-thetres-container"]/div[@class="theatre"]', timeout=timedelta(seconds=1))
            all_cinema_info = self.browser.find_elements('//div[@class="box-thetres-container"]/div[@class="theatre"]')
            for cinema in all_cinema_info:
                cinema_name = self.browser.find_element('xpath:.//h4', parent=cinema).text
                cinema_direction = self.browser.find_element('xpath:.//p[descendant::i[@class="icon-map-marker"]]', parent=cinema).text
                self.cinema_information.append({"Cinema":cinema_name, "Direction":cinema_direction})
        except SeleniumLibrary.errors.ElementNotFound:
            log_message("Had a problem getting the cinema information")
        log_message("End - Gets the cinema information")

    def get_cinema_schedule(self):
        """
        Opens each cinema and gets all the movies that they have scheduled
        """
        log_message("Start - Get cinema schedule")
        
        all_cinemas = self.browser.find_elements('//div[@class="theatre"]/a')
        self.browser.execute_javascript("window.open()")
        self.browser.switch_window(locator = "NEW")
        tabs_dict["Cinema"] = len(tabs_dict)
        try:
            for cinema in all_cinemas:
                cinema_data_dict = {}
                self.browser.switch_window(locator = self.browser.get_window_handles()[tabs_dict["Cinemark"]])
                self.browser.wait_until_element_is_visible('//div[@class="theatre"]/a', timeout=timedelta(seconds=1))
                cinema_link = self.browser.find_element(cinema).get_attribute("href")
                self.browser.switch_window(locator = self.browser.get_window_handles()[tabs_dict["Cinema"]])
                self.browser.go_to(cinema_link)
                self.browser.wait_until_element_is_visible('//div[@class="grid-center-content-vertical"]', timeout=timedelta(seconds=1))
                cinema_name = self.browser.find_element('//div[@class="grid-center-content-vertical"]//span').text
                print("Checking schedule of {}".format(cinema_name))
                movie_sections = self.browser.find_elements('//div[@class="grid-center-content"]/button')
                movie_list = []
                for section in movie_sections:
                    self.browser.click_element(section)
                    section_name = section.text
                    if section_name == "PREVENTA":
                        #Get all Preventa Movies
                        presale_movies = self.browser.find_elements('//ul[@class="container-preventa-covers"]/li')
                        for presale_movie in presale_movies:
                            self.browser.click_element(presale_movie)
                            total_movie_list = get_single_schedule(self.browser, section_name, movie_list)
                    else:
                        total_movie_list = get_single_schedule(self.browser, section_name, movie_list)
                cinema_data_dict[cinema_name] = total_movie_list
                self.movie_data_dict_list.append(cinema_data_dict)
                log_message("Finished {}".format(cinema_name))
        except SeleniumLibrary.errors.ElementNotFound:
            log_message("Had a problem getting the schedule information")
        print("Movie Information:",self.movie_information)   
        print("Cinema Data:",self.cinema_information)   
        print("Movie Data:",self.movie_data_dict_list)    
        log_message("End - Get cinema schedule")

    def create_excel(self):
        """
        Create the Excel file with the information
        """
        #Given the list of dictionaries, create the Excel with all the information
        log_message("Start - Create Excel")
        files.create_workbook(path = os.path.join(OUTPUT_FOLDER, "Cinemark.xlsx"))
        files.create_worksheet(name = "Movies", content= None, exist_ok = True, header = False)
        files.append_rows_to_worksheet(self.movie_information, name = "Movies", header = True, start= None)
        files.create_worksheet(name = "Cinemas", content= None, exist_ok = True, header = False)
        files.append_rows_to_worksheet(self.cinema_information, name = "Cinemas", header = True, start= None)
        for movie_data_dict in self.movie_data_dict_list:
            for key, value in movie_data_dict.items():
                files.create_worksheet(name = key, content= None, exist_ok = True, header = False)
                files.append_rows_to_worksheet(value, name = key, header = True, start= None)
        files.remove_worksheet(name = "Sheet")
        files.save_workbook(path = None)
        files.close_workbook()
        log_message("End - Create Excel")
