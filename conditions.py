import pandas as pd
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
import csv

listOfCities = []

with open(r'YOURLOCATION/miasta w Polsce.csv', newline='') as inputfile:
    for row in csv.reader(inputfile):
        listOfCities.append(row[0])
 
places = []
latitudes = []
longitudes = []
obscuration = []
magnitude = []
        
driver = webdriver.Firefox(executable_path=r"YOURLOCATION/geckodriver.exe")
time.sleep(5)
driver.get("https://www.heavens-above.com/")
time.sleep(5)

for i in range(len(listOfCities)):
     
    driver.find_element_by_xpath('//*[@id="ctl00_linkLatLong"]').click() #go to location change page
    time.sleep(2)
    searchbox = driver.find_element_by_xpath('//*[@id="ctl00_cph1_txtAddress"]')
    searchbox.send_keys(f"{listOfCities[i]}")
    time.sleep(2)
    searchbox.send_keys(Keys.ENTER)
    time.sleep(2)
    
    try:
        place = driver.find_element_by_xpath("/html/body/form/table/tbody/tr[3]/td[1]/div/table/tbody/tr[2]/td[2]/select/option[1]").text
    except:
        place = "Error"
    try:
        lat = driver.find_element_by_xpath("/html/body/form/table/tbody/tr[3]/td[1]/table[2]/tbody/tr[1]/td[2]/input").get_attribute("value")
    except:
        lat = "Error"
    try:
        lon = driver.find_element_by_xpath("/html/body/form/table/tbody/tr[3]/td[1]/table[2]/tbody/tr[2]/td[2]/input").get_attribute("value")
    except:
        lon = "Error"
    
    driver.find_element_by_xpath('//*[@id="ctl00_cph1_btnSubmit"]').click() #confirmation of location change
    time.sleep(2)
        
    try:
        driver.get("https://www.heavens-above.com/SolarEclipseLocal.aspx?jdmax=2459375.94660477") #go to the eclipse info page
    except:
        pass
    try:
        obs = float(driver.find_element_by_xpath('/html/body/form/table/tbody/tr[3]/td[1]/div[2]/div[1]/div[2]/div/div[2]/table/tbody/tr[4]/td[2]').text[:-1].replace(",", "."))
    except:
        obs = "Error"
    try:
        magn = float(driver.find_element_by_xpath('/html/body/form/table/tbody/tr[3]/td[1]/div[2]/div[1]/div[2]/div/div[2]/table/tbody/tr[3]/td[2]').text.replace(",", "."))
    except:
        magn = "Error"
        
    places.append(place)
    latitudes.append(lat)
    longitudes.append(lon)
    obscuration.append(obs)
    magnitude.append(magn)
        
    time.sleep(2)
        
driver.quit()

df = pd.DataFrame(list(zip(listOfCities, places, latitudes, longitudes, obscuration, magnitude)), columns = ["City", "Place found", "Latitude", "Longitude", "Obscuration", "Magnitude"])
df.to_csv("FILENAME.csv", sep = ";")
