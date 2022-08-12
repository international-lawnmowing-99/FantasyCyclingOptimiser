from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.firefox.options import Options

import pandas as pd
#pd.set_option('display.max_colwidth', None)
#pd.set_option('display.max_columns', None)

import re
import datetime
import sys

print (sys.version)

options = Options()
options.headless = False

DRIVER_PATH = 'geckodriver.exe'
driver = webdriver.Firefox(options=options, executable_path=DRIVER_PATH)

driver.install_addon("C:\\Users\\Alexander Peters\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\4ssj22zm.default\\extensions\\uBlock0@raymondhill.net.xpi", temporary=True)

def ScrapeRider(riderThing):
    driver.get(riderThing[2])
    riderInfoContainer = driver.find_element_by_class_name("rdr-info-cont")

    points = riderInfoContainer.find_elements_by_class_name("pnt")

    ODIPoints = points[0].text
    GCPoints = points[1].text
    TTPoints = points[2].text
    sprintPoints = points[3].text
    climbingPoints = points[4].text
    # print(riderInfoContainer.text)
    riderInfoContainer = riderInfoContainer.text.splitlines()

    ageTextLine = riderInfoContainer[0]
    if " (" in ageTextLine:
        dateString = ageTextLine[ageTextLine.find(":")+2 : ageTextLine.find(" (")]
    else:
        dateString = ageTextLine[ageTextLine.find(":")+2 : ]

    fuck = dateString.split()

    day = re.sub('(st|nd|rd|th)', '', fuck[0])
    month = fuck[1]
    year = fuck[2]

    if len(day) == 1:
        day = "0"+day

    parsedDate = datetime.datetime.strptime(day + " " + month + " " + year, '%d %B %Y')
    #print(parsedDate)

    nation = riderInfoContainer[1][riderInfoContainer[1].find("Nationality: ") + 13:]
    # print(nation)
    weight = riderInfoContainer[2][riderInfoContainer[2].find("Weight: ") + 8: riderInfoContainer[2].find(" kg")]
    # print(weight)
    height = riderInfoContainer[2][riderInfoContainer[2].find("Height: ") + 8 : riderInfoContainer[2].find(" m")]
    # print(height)

    keyStats = driver.find_element_by_class_name("rider-kpi").find_elements_by_tag_name("li")#"right w25 mb_w100")
    totalWins = keyStats[0].find_element_by_class_name("nr   ").text
    #print(totalWins)
    # if(totalWins.text == "0"):
    #     GCWins = 0
    #     ODIWins = 0
    #     TTWins = 0
    # else:
    #     wins = keyStats[0].find_elements_by_tag_name("div")
    #     print(wins)
    #     GCWins = wins[0]
    #
    #     ODIWins = wins[1]
    #     TTWins = wins[2]
    # print(GCWins.text)
    # print(ODIWins.text)
    # print(TTWins.text)

    grandTourParticipations = keyStats[1].find_element_by_class_name("nr   ").text
    #print (grandTourParticipations.text)
    classicsParticipations = keyStats[2].find_element_by_class_name("nr   ").text
    #print (classicsParticipations.text)

    yearlyStatsTable = driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[8]/div[1]/div[4]/div[2]/table")
    tableRows = yearlyStatsTable.find_elements_by_tag_name("tr")

    riderThing+= [ODIPoints, GCPoints, TTPoints, sprintPoints, climbingPoints, parsedDate, nation, weight, height, totalWins, grandTourParticipations, classicsParticipations]

    for row in tableRows[1:]:
        year = row.find_element_by_class_name("season  ").text
        points = row.find_element_by_xpath(".//td[2]/div/span").text
        position = row.find_element_by_class_name("ac  ").text
        riderThing.append([year,points,position])

    for i in range(35-len(tableRows[1:])):
        riderThing.append([0,0,0])

def ScrapeStages(currentYear):
    driver.get("https://www.procyclingstats.com/race/tour-de-france/" + str(currentYear) + "/stages/winners")
    

def ScrapeTeams(currentYear):
        print("Scraping teams for " + str(currentYear))
        driver.get("https://www.procyclingstats.com/race/tour-de-france/" + str(currentYear) + "/startlist/startlist")

        data = []


        teams = driver.find_elements_by_class_name("team")
        #print (len(teams))

        for team in teams:
            teamName = team.find_element_by_xpath(".//b/a").text

            riders = team.find_elements_by_css_selector("li")
            for rider in riders:
                shirtNumber = int(rider.text.split()[0])
                #print(shirtNumber)
                teamLeader = False
                if int(shirtNumber)%10==1:
                     teamLeader = True
                blue = rider.find_element_by_class_name("blue")
                data.append([blue.text, teamName, blue.get_attribute("href"), shirtNumber, teamLeader])

        for i in range(int(len(data))):
                ScrapeRider(data[i])
            #allRiders = allRiders.append(df1[df1[])
            #print(data[i])

        df = pd.DataFrame(data)#, columns = ["Rider", "Team", "URL", "Shirt Number", "Notional Team Leader?", "ODIPoints", "GCPoints", "TTPoints", "sprintPoints", "climbingPoints", "parsedDate", "nation", "weight", "height", "totalWins", "grandTourParticipations", "classicsParticipations", "yearsPointsPosition"])#, "Age", "Nation", "Weight", "Height"])
        print(df.head())

        df.to_csv("data/TDFStartlists/dataTDF" + str(currentYear) + ".csv")



for q in range(15):
    currentYear = 2007 + q
    ScrapeStages(currentYear)

driver.quit()
