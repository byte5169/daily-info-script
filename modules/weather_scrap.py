import requests
import pandas as pd

from bs4 import BeautifulSoup

page = requests.get("https://pogoda.tut.by/")
soup = BeautifulSoup(page.content, "html.parser")
forecast = soup.find(id="simple_mode")
forecast_items = forecast.find_all(class_="b-forecast-top")
this_time = forecast_items[0]
period = this_time.find(class_="b-forecast-top__time").get_text()
temp_now = this_time.find(class_="b-forecast-top__temp").get_text()
temp_state = this_time.find(class_="b-forecast-add").get_text()
temp_feel = this_time.find(class_="b-forecast-more").get_text().split('\n')

temp_descs = [sd.get_text() for sd in forecast.select(".b-forecast-top .b-forecast-top__temp")]
period_descs = [sd.get_text() for sd in forecast.select(".b-forecast-top .b-forecast-top__time")]
state_descs = [t.get_text() for t in forecast.select(".b-forecast-top .b-forecast-add")]


weather = pd.DataFrame({
    "period": period_descs,
    "temp_descs": temp_descs,
    "temp_state":state_descs,
})
print(weather.iloc[0,1])
print(temp_feel)