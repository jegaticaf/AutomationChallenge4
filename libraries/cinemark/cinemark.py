from libraries.common import log_message, files, convert_string_to_date, regex_money
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
        time.sleep(1)
        self.browser.click_element('//button[text()="Aceptar"]')

        log_message("End - Access Cinemark.pe")

    def go_to_section(self, parameter:str):
        """
        Go to the section that is given as a parameter
        """
        log_message("Start - Go to section {}".format(parameter))
        self.browser.switch_window(locator = self.browser.get_window_handles()[tabs_dict["Cinemark"]])
        self.browser.go_to(self.cinemark_url)
        self.browser.click_element('//ul[@class="box-menu grid-center-content"]//a[text()="{}"]'.format(parameter))
        time.sleep(1)
        log_message("End - Go to section {}".format(parameter))

    def extract_movies_data(self):
        """
        Goes to each of the movies sections and takes all the information of each movie.
        """
        log_message("Start - Extract the movies information")
        self.browser.click_element('//button[text()="Cartelera"]')
        time.sleep(3)
        current_movies = self.browser.find_elements('//div[@class="movies-container row-margin-bottom col-lg-12"]/div[@class="movie-box-container"]')
        self.browser.execute_javascript("window.open()")
        self.browser.switch_window(locator = "NEW")
        tabs_dict["Movie"] = len(tabs_dict)
        for movie in current_movies:
            self.browser.switch_window(locator = self.browser.get_window_handles()[tabs_dict["Cinemark"]])
            movie_link = self.browser.find_element('xpath:.//a', parent=movie).get_attribute("href")
            self.browser.switch_window(locator = self.browser.get_window_handles()[tabs_dict["Movie"]])
            self.browser.go_to(movie_link)
            time.sleep(1)
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
            time.sleep(1)
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
            time.sleep(1)
            movie_title = self.browser.find_element('//div[@class="row movie-trailer-content"]//h1').text
            movie_data = self.browser.find_elements('//div[@class="movie-details"]//li')
            movie_rating = self.browser.find_element(movie_data[0]).text
            movie_duration = self.browser.find_element(movie_data[1]).text
            self.movie_information.append({"Title": movie_title, "Duration": movie_duration, "Rating": movie_rating})
        log_message("Finished the coming soon movies")

        log_message("End - Extract the movies information")

    def extract_cinema_data(self):
        """
        Gets the information for every cinema
        """
        log_message("Start - Gets the cinema information")
        self.browser.click_element('//button[@class="more-theatres"]')
        time.sleep(1)
        all_cinema_info = self.browser.find_elements('//div[@class="box-thetres-container"]/div[@class="theatre"]')
        for cinema in all_cinema_info:
            cinema_name = self.browser.find_element('xpath:.//h4', parent=cinema).text
            cinema_direction = self.browser.find_element('xpath:.//p[descendant::i[@class="icon-map-marker"]]', parent=cinema).text
            self.cinema_information.append({"Cinema":cinema_name, "Direction":cinema_direction})
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

        for cinema in all_cinemas:
            cinema_data_dict = {}
            self.browser.switch_window(locator = self.browser.get_window_handles()[tabs_dict["Cinemark"]])
            cinema_link = self.browser.find_element(cinema).get_attribute("href")
            self.browser.switch_window(locator = self.browser.get_window_handles()[tabs_dict["Cinema"]])
            self.browser.go_to(cinema_link)
            time.sleep(1)
            cinema_name = self.browser.find_element('//div[@class="grid-center-content-vertical"]//span').text
            print("Checking schedule of {}".format(cinema_name))
            movie_sections = self.browser.find_elements('//div[@class="grid-center-content"]/button')
            movie_list = []
            for section in movie_sections:
                self.browser.click_element(section)
                section_name = section.text
                all_days = self.browser.find_elements('//ul[@class="billboard-days"]//button')
                for day in all_days:
                    day_part_1 = self.browser.find_element('xpath:.//h3', parent=day).text
                    day_part_2 = self.browser.find_element('xpath:.//h5', parent=day).text
                    current_date = "{} {}".format(day_part_1,day_part_2)
                    self.browser.click_element(day)
                    time.sleep(1)
                    all_movies = self.browser.find_elements('//div[@class="movie-box row"]')
                    for movie in all_movies:
                        movie_name = self.browser.find_element('xpath:.//div[@class="movie-title"]/a', parent=movie).text
                        movie_data = self.browser.find_elements('xpath:.//div[@class="movie-details"]//li', parent=movie)
                        movie_rating = self.browser.find_element(movie_data[0]).text
                        movie_duration = self.browser.find_element(movie_data[1]).text
                        movie_dict = {"Movie name": movie_name, "Runtime": movie_duration, "Rating": movie_rating, "Date": current_date, "Type": section_name}
                        movie_list.append(movie_dict)
                        movie_versions = self.browser.find_elements('xpath:.//div[@class="movie-version"]/span', parent=movie)
                        movie_versions_list = [version.text for version in movie_versions]
                        movie_language = self.browser.find_element('xpath:.//div[@class="movie-lenguaje"]/span', parent=movie).text
                        movie_seat_types = self.browser.find_elements('xpath:.//div[@class="movie-seats"]/span', parent=movie)
                        movie_seat_types_list = [seat_type.get_attribute("class").split("-")[-1] for seat_type in movie_seat_types[1:]]
                        movie_showtimes = self.browser.find_elements('xpath:.//div[@class="movie-times"]/a', parent=movie)
                        movie_showtimes_list = [showtime.text for showtime in movie_showtimes]
                        movie_full_info_dict = {"version": movie_versions_list, "language": movie_language, 
                        "seat types": movie_seat_types_list, "showtimes": movie_showtimes_list}
                        print("{}:\n{}".format(movie_name,movie_full_info_dict))
            cinema_data_dict[cinema_name] = movie_list
            self.movie_data_dict_list.append(cinema_data_dict)
            log_message("Finished {}".format(cinema_name))
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