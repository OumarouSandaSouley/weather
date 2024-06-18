from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.core.window import Window
import requests 
from bs4 import BeautifulSoup
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton

Window.size = {400, 600}



class WeatherApp(MDApp):

    dialog = None

    api_key = '81d5797a596c5eb5d9e79d5d23070266'

    def open_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title = 'Offline alert',
                text = 'It seems that you are offline, check your internet connection and try again !!!',
                
                buttons = [
                    MDFlatButton(
                        text = 'Ok'
                    )
                ]
            )
        self.dialog.open()

    def on_start(self):
        try:

            soup = BeautifulSoup(requests.get(f"https://www.google.com/search?q=weather+at+my+current+location").text, "html.parser")
            temp = soup.find("span", class_= "BNeawe tAd8D AP7Wnd")
            location = ''.join(filter(lambda item: not item.isdigit(), temp.text)).split(",", 1)
            self.get_weather(location[0])
        except requests.ConnectionError:
            print('No internet connextion')
            self.open_dialog()


    def build(self):
        self.icon = "img/logo.png"
        self.theme_cls.primary_palette = 'Blue'
        screen  = Builder.load_file('screen/screen.kv')
        return  screen
    

    def get_weather(self, city_name):
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={self.api_key}"
            res = requests.get(url)
            x = res.json()
            if x["cod"] != "404":
                temperature = round(x["main"]["temp"] -273.15)
                humididty = x["main"]["humidity"]
                weather = x["weather"][0]["main"]
                id = str(x["weather"][0]["id"])
                wind_speed = round(x["wind"]["speed"]*18/5)
                location = x["name"] + ", " + x["sys"]["country"]
                self.root.ids.temperature.text = f"[b]{temperature}[/b]°"
                self.root.ids.weather.text = str(weather)
                self.root.ids.humidity.text = f"{humididty}%"
                self.root.ids.wind_speed.text = f"{wind_speed} km/h"
                self.root.ids.location.text = location
                if id == "800":
                    self.root.ids.weather_img.source = "img/sun.png"
                elif "200" <= id <= "232":
                    self.root.ids.weather_img.source = "img/storm.png"
                elif "300" <= id <= "321" or "500" <= id <= "521" :
                    self.root.ids.weather_img.source = "img/rain.png"
                elif "600" <= id <= "622":
                    self.root.ids.weather_img.source = "img/snow.png"
                elif "701" <= id <= "781":
                    self.root.ids.weather_img.source = "img/haze.png"
                elif "801" <= id <= "804":
                    self.root.ids.weather_img.source = "img/clouds.png"
            else:
                print('city not found')
        except requests.ConnectionError:
            print('No internet connection')
            self.open_dialog()

    def search_weather(self):
        city_name = self.root.ids.city_name.text
        if city_name != "":
            self.get_weather(city_name)








if __name__=="__main__":
    WeatherApp().run()