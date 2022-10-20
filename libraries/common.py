import shutil, time, os, re
from robot.api import logger
from datetime import datetime, timedelta
from RPA.Browser.Selenium import Selenium
from RPA.Excel.Files import Files
from RPA.FileSystem import FileSystem
from config import OUTPUT_FOLDER
import SeleniumLibrary.errors

browser = Selenium()
files = Files()
file_system = FileSystem()

def log_message(message: str, level: str = "INFO", console: bool = True):
    """
    Function that logs messages depending on the level
    """
    log_switcher = {"TRACE": logger.trace, "INFO": logger.info, "WARN": logger.warn, "ERROR": logger.error}

    if not level.upper() in log_switcher.keys() or level.upper() == "INFO":
        logger.info(message, True, console)
    else:
        if level.upper() == "ERROR":
            logger.info(message, True, console)
        else:
            log_switcher.get(level.upper(), logger.error)(message= True)

def print_version():
    """
    Function that prints the version of the project
    """
    try:
        file = open("VERSION")
        try:
            print("Version {}".format(file.read().strip()))
        except Exception as e:
            print("Error reading VERSION file: {}".format(str(e)))
        finally:
            file.close()
    except Exception as e:
        log_message("VERSION file not found: {}".format(str(e)))

def create_or_clean_dir(folder_path: str):
    """
    Function that cleans and creates a determined folder
    """
    shutil.rmtree(folder_path, ignore_errors= True)
    try:
        os.mkdir(folder_path)
    except FileExistsError:
        pass

def capture_page_screenshot(folder_path: str, name: str = "None"):
    """
    Function that captures a screenshot of the browser
    """
    if not name:
        name = "Exception_{}.png".format(datetime.now().strftime("%H_%M_%S"))
    else:
        name = "{}_{}.png".format(name, datetime.now().strftime("%H_%M_%S"))

    browser.capture_page_screenshot(os.path.join(folder_path, name))

def get_single_schedule(browser, section_name:str, movie_list:list):
    """
    Gets all the dates and movies for a single section
    """
    all_days = browser.find_elements('//ul[@class="billboard-days"]//button')
    for day in all_days:
        try:
            day_part_1 = browser.find_element('xpath:.//h3', parent=day).text
            day_part_2 = browser.find_element('xpath:.//h5', parent=day).text
            current_date = "{} {}".format(day_part_1,day_part_2)
            browser.click_element(day)
            time.sleep(1)
            all_movies = browser.find_elements('//div[@class="movie-box row"]')
            for movie in all_movies:
                try:
                    movie_name = browser.find_element('xpath:.//div[@class="movie-title"]/a', parent=movie).text
                    movie_data = browser.find_elements('xpath:.//div[@class="movie-details"]//li', parent=movie)
                    movie_rating = browser.find_element(movie_data[0]).text
                    movie_duration = browser.find_element(movie_data[1]).text
                    movie_dict = {"Movie name": movie_name, "Runtime": movie_duration, "Rating": movie_rating, "Date": current_date, "Type": section_name}
                    movie_list.append(movie_dict)
                    movie_versions = browser.find_elements('xpath:.//div[@class="movie-version"]/span', parent=movie)
                    movie_versions_list = [version.text for version in movie_versions]
                    movie_language = browser.find_element('xpath:.//div[@class="movie-lenguaje"]/span', parent=movie).text
                    movie_seat_types = browser.find_elements('xpath:.//div[@class="movie-seats"]/span', parent=movie)
                    movie_seat_types_split = [seat_type.get_attribute("class").split("-")[-1] for seat_type in movie_seat_types[1:]]
                    movie_seat_types_list = [seat_type for seat_type in movie_seat_types_split if seat_type != ""]
                    movie_showtimes = browser.find_elements('xpath:.//div[@class="movie-times"]/a', parent=movie)
                    movie_showtimes_list = [showtime.text for showtime in movie_showtimes]
                    movie_full_info_dict = {"version": movie_versions_list, "language": movie_language, 
                    "seat types": movie_seat_types_list, "showtimes": movie_showtimes_list}
                except SeleniumLibrary.errors.ElementNotFound as ex:
                    log_message(str(ex))
            print(movie_full_info_dict)
        except SeleniumLibrary.errors.ElementNotFound as ex:
                log_message(str(ex))
    return movie_list