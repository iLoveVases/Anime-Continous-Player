from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from wbijam.locator import *
from selenium.webdriver.support.wait import WebDriverWait  # for Explicit Wait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs


class Wbijam:
    def __init__(self, teardown=False):
        self.episodes_list = None
        self.episode_number = None
        self.players_list = None
        self.player_name = None
        self.anime_name = None
        self.horizontal = None
        self.teardown = teardown
        self.options = Options()
        self.options.add_experimental_option("detach", True)
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

    def choose_episode(self, episode_number='011'):
        self.episode_number = str(episode_number)
        self.episodes_list = self.driver.find_elements(By.CLASS_NAME, "lista_hover")

        for episode in self.episodes_list:
            if self.episode_number in episode.text.split(":")[0]:
                print(episode.text.split(":")[0])
                episode.find_element(By.TAG_NAME, 'a').click()
                break


        # self.html = self.driver.page_source
        # soup = bs(self.html, "html.parser")


        # self.driver.find_element(By.XPATH, "//*[@id=\"tresc_lewa\"]/table/tbody/tr[3]/td[5]/span").click()
        # self.driver.implicitly_wait(15) #self.driver.find_element(By.CLASS_NAME, "pb pb-play").click()
        # self.driver.switch_to.frame( self.driver.find_element(By.XPATH, "//iframe[contains(@src https://ebd.cda.pl/640x526/1027824519")]))
        #                                         WebDriverWait(self.driver, 10).until(
        # EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[1]/div/div/div/div/div/div/div/span[4]/span/span[
        # 1]"))).click()

    def choose_player(self, player_name="cda"):
        self.player_name = player_name
        self.players_list = self.driver.find_elements(By.CLASS_NAME, "lista_hover")

        for player in self.players_list:
            if self.player_name in player.text:
                print(player.text)
                player.find_element(By.CLASS_NAME, "odtwarzacz_link").click()
                break

