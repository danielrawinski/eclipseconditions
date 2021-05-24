import pandas as pd
import requests
import datetime
import time

df = pd.read_csv(r"YOURLOCATION/poland_eclipses_ha_corrected_with_coords.csv", sep = ";")

clouds = []
 
for i in range(len(df)):
    request = requests.get(f"https://api.openweathermap.org/data/2.5/onecall?lat={df.iloc[i]['Latitude']}&lon={df.iloc[i]['Longitude']}&exclude=current,minutely,hourly,alerts&appid=yourapikey")
    requestJson = request.json()
    
    clouds.append(requestJson["daily"][3]["clouds"])
    
    time.sleep(1)
    
df["Clouds"] = clouds    
del clouds

print(range(len(df)))

results = df.loc[(df["Clouds"] <= 50)].sort_values(by=["Magnitude"], ascending=False) #50 is an arbitrary cut-off value
