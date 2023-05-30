from selenium.webdriver.common.by import By


class MainPage(object):
    MAIN_PAGE = "https://www.wbijam.pl"
    COOKIE_BUTTON_1 = (By.XPATH, "/html/body/div[12]/div[1]/div[2]/div/div[2]/button[2]")
    COOKIE_BUTTON_2 = (By.ID, "simplecookienotificationokbutton")
    BLEACH = (By.XPATH, "/html/body/div[2]/a[8]")
    BLUE_LOCK = (By.XPATH, "/html/body/div[2]/a[9]")