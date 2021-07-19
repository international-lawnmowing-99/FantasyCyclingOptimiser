import requests
from bs4 import BeautifulSoup
from rider import Rider
from pulp import *

bestTeam = LpProblem("Cycling_Optimiser", LpMaximize)
worstTeam = LpProblem("Cycling_Optimiser", LpMinimize)

allRiders = []



def ScrapeFinalValues(URL):
        page = requests.get(URL)

        soup = BeautifulSoup(page.content, 'html.parser')

        rows = soup.find('tbody').find_all("tr")
        for row in rows:
            tds = row.find_all("td")

            # 1 = name
            # 2 = team
            # 3 = category
            # 4 = cost
            # 6 = total points
            #get the first name and last name together as before by stepping through the workbook
            #when this matches that value, get the index, and add the relevant info to the sheet
            rider = Rider()

            rider.name = tds[1].text
            rider.riderCategory = tds[3].text
            rider.cost = int(tds[4].text)
            rider.totalPoints = int(tds[6].text)

            allRiders.append(rider)

def CreateModels(best, worst):
    function = ""
    costConstraint = ""
    allRounderConstraint = ""
    sprinterContraint = ""
    climberConstraint = ""
    unclassedConstrant = ""
    numberOfRidersConstraint = ""
    variables = []

    for rider in allRiders:
        variable = LpVariable(rider.name, 0,1,LpInteger)
        variables.append(variable)
        function +=  rider.totalPoints * variable
        costConstraint += rider.cost * variable
        numberOfRidersConstraint += variable

        if rider.riderCategory == "All Rounder":
            allRounderConstraint += variable
        elif rider.riderCategory == "Climber":
            climberConstraint += variable
        elif rider.riderCategory == "Unclassed":
            unclassedConstrant += variable
        elif rider.riderCategory == "Sprinter":
            sprinterContraint += variable


    best += function

    best += (costConstraint <= 100)
    best += (numberOfRidersConstraint == 9)
    best += (sprinterContraint >= 1)
    best += (climberConstraint >= 2)
    best += (unclassedConstrant >= 3)
    best += (allRounderConstraint >= 2)


    worst += function

    worst += (costConstraint <= 100)
    worst += (numberOfRidersConstraint == 9)
    worst += (sprinterContraint >= 1)
    worst += (climberConstraint >= 2)
    worst += (unclassedConstrant >= 3)
    worst += (allRounderConstraint >= 2)

def FindBestTeam():
    print("\n\nFinding BEST Team: \n")
    optimization_result = bestTeam.solve()

    assert optimization_result == LpStatusOptimal
    print("Status:", LpStatus[bestTeam.status])
    print("Optimal Solution to the problem: ", value(bestTeam.objective))
    print ("Individual decision_variables: ")
    for v in bestTeam.variables():
        if v.varValue == 1:
            print(v)

def FindWorstTeam():
    print("\n\nFinding WORST Team: \n")
    optimization_result = worstTeam.solve()

    assert optimization_result == LpStatusOptimal
    print("Status:", LpStatus[worstTeam.status])
    print("Optimal Solution to the problem: ", value(worstTeam.objective))
    print ("Individual decision_variables: ")
    for v in worstTeam.variables():
        if v.varValue == 1:
            print(v)

if __name__ == '__main__':
    ScrapeFinalValues("https://www.velogames.com/velogame/2021/riders.php")
    CreateModels(bestTeam, worstTeam)
    FindBestTeam()
    FindWorstTeam()
