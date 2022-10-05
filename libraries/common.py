import shutil, os
from robot.api import logger
from datetime import datetime
from RPA.Browser.Selenium import Selenium
from RPA.Excel.Files import Files
from RPA.FileSystem import FileSystem
from config import OUTPUT_FOLDER

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
