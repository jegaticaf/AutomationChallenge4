from libraries.common import log_message, capture_page_screenshot, browser
from config import OUTPUT_FOLDER, tabs_dict
from libraries.cinemark.cinemark import Cinemark

class Process():
    
    def __init__(self, credentials: dict):
        log_message("Initialization")

        prefs = {
            "profile.default_content_setting_values.notifications": 2,
            "profile.default_content_setting_popups": 0,
            "directory_upgrade": True,
            "download.default_directory": OUTPUT_FOLDER,
            "plugins.always_open_pdf_externally": True,
            "download.prompt_for_download": False
        }

        browser.open_available_browser(preferences = prefs)
        browser.set_window_size(1920, 1080)
        browser.maximize_browser_window()

        cinemark = Cinemark(browser, {"url": "https://www.cinemark-peru.com/"})
        tabs_dict["Cinemark"] = len(tabs_dict)
        cinemark.access_cinemark()
        self.cinemark = cinemark

    def start(self):
        """
        main
        """

        self.cinemark.go_to_section("Películas")
        self.cinemark.extract_movies_data()
        self.cinemark.go_to_section("Cines")
        self.cinemark.extract_cinema_data()
        self.cinemark.get_cinema_schedule()
        self.cinemark.create_excel()

    
    def finish(self):
        log_message("DW Process Finished")
        browser.close_browser()