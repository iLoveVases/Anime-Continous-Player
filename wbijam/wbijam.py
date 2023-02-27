from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from wbijam.locator import *
from selenium.webdriver.support.wait import WebDriverWait  # for Explicit Wait
from selenium.webdriver.support import expected_conditions as EC
import time


class Wbijam:
    def __init__(self, teardown=False):

        self.actual_time = None
        self.buttons_bar = None
        self.current_player_iframe = None
        self.iframes = None
        self.episodes_list = None
        self.episode_number = None
        self.players_list = None
        self.player_name = None
        self.anime_name = None
        self.horizontal = None
        self.teardown = teardown
        self.options = Options()
        self.options.add_experimental_option("detach", True)
        self.options.add_experimental_option("useAutomationExtension", False)
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                                       options=self.options)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.driver.quit()

    def __enter__(self):
        return self

    def set_window(self, horizontal=0):
        self.horizontal = horizontal
        self.driver.set_window_position(self.horizontal, 0)
        self.driver.maximize_window()

    def land_main_page(self):
        self.driver.get(MainPage.MAIN_PAGE)

        try:
            cookie_one = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(MainPage.COOKIE_BUTTON_1)
            )
            cookie_one.click()

            cookie_two = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(MainPage.COOKIE_BUTTON_2)
            )
            cookie_two.click()
        except:
            print("No Cookie pop-up")

    def choose_anime(self, anime_name="Bleach"):
        self.anime_name = anime_name
        self.driver.find_element(By.LINK_TEXT, self.anime_name).click()
        self.driver.implicitly_wait(5)
        self.driver.find_element(By.LINK_TEXT, "Pierwsza seria").click()

    def choose_episode(self, episode_number='040'):  # jakis bug z 024
        self.episode_number = str(episode_number)
        self.episodes_list = self.driver.find_elements(By.CLASS_NAME, "lista_hover")

        for episode in self.episodes_list:
            if self.episode_number in episode.text.split(":")[0]:
                print(episode.text.split(":")[0])
                episode.find_element(By.TAG_NAME, 'a').click()
                break

    def choose_player(self, player_name="cda"):
        self.player_name = player_name
        self.players_list = self.driver.find_elements(By.CLASS_NAME, "lista_hover")

        for player in self.players_list:
            if self.player_name in player.text:
                print(player.text)
                player.find_element(By.CLASS_NAME, "odtwarzacz_link").click()
                break

    def play(self):
        self.iframes = self.driver.find_elements(By.TAG_NAME, 'iframe')
        for iframe in self.iframes:
            if "cda" in iframe.get_attribute('src'):
                print(iframe.get_attribute('src'))
                self.current_player_iframe = iframe
                break

        self.driver.switch_to.frame(self.current_player_iframe)

        try:
            # Waiting for player's button's bar to appear
            bar = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "button-players"))
            )
            self.buttons_bar = bar
        finally:
            self.buttons_bar.find_element(By.CLASS_NAME, "pb.pb-play").click()
            self.buttons_bar.find_element(By.CLASS_NAME, "pb.pb-fullscreen").click()

        # time.sleep(3)
        # self.actual_time = self.buttons_bar.find_element(By.CLASS_NAME, "pb-actual-time").text
        # print(str(self.actual_time))

        self.driver.switch_to.default_content()
