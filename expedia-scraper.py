import bs4
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import contextlib
# import selenium.webdriver as webdriver
import selenium.webdriver.support.ui as ui

originCity = 'LAX'
destinationCity = 'CLT'
majorCities = ['NYC','CHI','ATL','BOS','MSP']

def checkDirect(origin, destination):
	with contextlib.closing(webdriver.Firefox()) as driver:
	  driver.get("http://www.expedia.com/Flights-Search?trip=oneway&leg1=from:" + origin + ",to:" + destination + ",departure:01/20/2015TANYT&passengers=children:0,adults:1,seniors:0,infantinlap:Y&mode=search")
	  try:
	    ui.WebDriverWait(driver, 15).until_not(EC.visibility_of_element_located((By.ID, "acol-interstitial")))
	  finally:
	    html = driver.page_source
	    soup = BeautifulSoup(html)
	    priceInfo = [soup.find_all('span', class_='price-emphasis')[0], soup.find_all('span', class_='price-emphasis')[1]]
	    lowestPrice = priceInfo[0].get_text()[1:] + priceInfo[1].get_text()
	    return lowestPrice


def checkMulti(origin, destination, majorCity, lowestPrice):
	with contextlib.closing(webdriver.Firefox()) as driver:
	  driver.get("http://www.expedia.com/Flights-Search?trip=oneway&leg1=from:" + origin + ",to:" + majorCity + ",departure:01/20/2015TANYT&passengers=children:0,adults:1,seniors:0,infantinlap:Y&mode=search")
	  try:
	    ui.WebDriverWait(driver, 15).until_not(EC.visibility_of_element_located((By.ID, "acol-interstitial")))
	  finally:
	    html = driver.page_source
	    soup = BeautifulSoup(html)
	    for tag in soup.find_all("div", class_="flex-card"):
		  	# all stop information
	      numStops = tag.find_all('div', class_='primary-block')[2].contents[1].get_text().strip()
		  	# if stop info is more than non-stop, get last three digits
	      if numStops != "Nonstop":
		  		# need to test for multi-stops
	        stopInfo = tag.find_all('div', class_='primary-block')[2].contents[3].get_text().strip()[-3:]
	        if stopInfo == destination:
	          priceInfo = tag.find_all('div', class_='offer-price')[0].find_all('span', class_='price-emphasis')
	          convertedPrice = priceInfo[0].get_text()[1:] + priceInfo[1].get_text()
	          if convertedPrice < lowestPrice:
	          	print 'yes', majorCity

theLowestPrice = checkDirect(originCity, destinationCity)
for city in majorCities:
	checkMulti(originCity, destinationCity, city, theLowestPrice)