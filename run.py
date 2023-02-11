from wbijam.wbijam import Wbijam

with Wbijam(teardown=False) as bot:
    bot.set_window(-1000)  # left monitor
    bot.land_main_page()
    bot.choose_anime(anime_name="Bleach")
    bot.choose_episode()
    bot.choose_player()
    print("eesa")