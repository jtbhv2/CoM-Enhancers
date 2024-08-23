#This one is upgraded. Sends using SMTP directly into city domain, directly to recipients.
#No need to manually forward anymore! Yay!
#WILL FAIL IF RUN WITHIN CITY NETWORK. CITY FIREWALL DOES NOT ALLOW SENDING OF SMTP. MUST RUN OUTSIDE NETWORK.

import pdfkit
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from datetime import datetime
import os
from redmail import gmail
import base64
import requests

# Gmail configuration
gmail.username = 'MemphisDailyWeather@gmail.com'
gmail.password = os.getenv('googlekey')

# memphis is hardcoded. change the urls to f strinngs to mod them to pull from anywhere
NWSURL = 'https://forecast.weather.gov/MapClick.php?lat=35.1495&lon=-90.0490&FcstType=json'

def getWeatherData(url):
    response = requests.get(url)
    response.raise_for_status()  # in retrospect this will probably be useful
    return response.json()

def forecastFormat(forecastData):
    periods = forecastData['time']['startPeriodName']
    temperatures = forecastData['data']['temperature']
    precipChance = forecastData['data']['pop']
    weatherConditions = forecastData['data']['weather']
    rainfallAmounts = forecastData['data'].get('precipitation', [None]*len(periods))

    todayIndex = periods.index('Today') if 'Today' in periods else -1

    if todayIndex == -1:
        return "No forecast data for today."

    todayTemp = temperatures[todayIndex]
    todayWeather = weatherConditions[todayIndex]
    todayPrecipChance = precipChance[todayIndex]
    todayRainfall = rainfallAmounts[todayIndex] if todayIndex < len(rainfallAmounts) else None

    #summary = f"Weather Summary for {datetime.now().strftime('%Y-%m-%d')}:\n"
    summary = f"Temperature: {todayTemp}°F\n"
    summary += f"Weather: {todayWeather}\n"
    summary += f"Chance of Precipitation: {todayPrecipChance}%\n"

    if todayRainfall is not None:
        summary += f"Expected Rainfall: {todayRainfall} inches\n"
        if todayRainfall >= 1:
            summary += "Recommend activating hotspots.\n"
        else:
            summary += "Hotspots not needed for today.\n"
    
    return summary

# grab some weather bby
weatherData = getWeatherData(NWSURL)
weatherSummary = forecastFormat(weatherData)

# Output paths. Same directory since they are getting deleted anyways
output1 = "page1.pdf"
output2 = "page2.pdf"

# first is the summary page, second is a close up of the graphs
url1 = "https://forecast.weather.gov/MapClick.php?lat=35.04218000000003&lon=-89.98156999999998"
url2 = "https://forecast.weather.gov/MapClick.php?lat=35.0422&lon=-89.9816&unit=0&lg=english&FcstType=graphical"

# grab that pdf
pdfkit.from_url(url1, output1)
pdfkit.from_url(url2, output2)

# more pdf things
reader1 = PdfReader(output1)
writer = PdfWriter()
writer.add_page(reader1.pages[0])
output1SinglePage = "page1firstpageonly"
with open(output1SinglePage, "wb") as f:
    writer.write(f)

# pdf merge time
merger = PdfMerger()
merger.append(output1SinglePage)
merger.append(output2)

# wild how complex this part was for me
currentDate = datetime.now().strftime("%Y-%m-%d")
outputPDF = f"WeatherFor{currentDate}.pdf"
merger.write(outputPDF)
merger.close()

# delete that extra shiiiiiii
os.remove(output1)
os.remove(output2)
os.remove(output1SinglePage)

# Email configuration
recipientEmail = 'brian.stlouis@memphistn.gov'
senderEmail = 'MemphisDailyWeather@gmail.com'
recipientCC = 'emailaddresshere'
recipientBCC = 'emailaddresshere'

with open(outputPDF, 'rb') as f:
    pdf_data = f.read()

# send email using gmail
try:
    gmail.send(
        subject=f'Weather Report for {currentDate}',
        receivers=[recipientEmail],
        #cc=[recipientCC], #set up for these juuuuuuuust in case
        #bcc=[recipientBCC],
        text=f'Weather Summary for {currentDate}:\n\n{weatherSummary}',
        attachments={outputPDF: pdf_data}
    )
    print("Email sent successfully")
except Exception as e:
    print(f"Failed to send email: {e}")
