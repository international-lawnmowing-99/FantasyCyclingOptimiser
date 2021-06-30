from rider import Rider
from openpyxl import load_workbook
import unicodedata
from openpyxl.worksheet import worksheet
workbook = load_workbook(filename="finalFinal.xlsx")
sheet = workbook["DYN_cyclist"]
pointsSheet = workbook["PointsSheet"]



riders = []

def totalSprintiness(lad):
    return lad.acceleration + lad.sprint

for i in range(183):
    r = Rider()
    nam = str(sheet.cell(i+2,2).value) + " " + str(sheet.cell(i+2,1).value)
    nam = deaccent(nam)
    r.name = nam
    r.acceleration= sheet.cell(i+2,10).value
    r.flat= sheet.cell(i+2,3).value
    r.hill= sheet.cell(i+2,14).value
    r.mountain= sheet.cell(i+2,4).value
    r.resistance= sheet.cell(i+2,12).value
    r.sprint= sheet.cell(i+2,9).value
    r.tt = sheet.cell(i+2,7).value
    r.downhill = sheet.cell(i+2, 5).value
    r.index = i + 2
    riders.append(r)




def SprintStage(StageNumber):
    riders.sort(key=lambda a: a.sprint + a.acceleration, reverse=True)
    #add points to the riders

    GiveWinPoints(StageNumber)
    AssignGCPoints(StageNumber)

def HillStage(StageNumber):

    riders.sort(key=lambda a: a.hill + a.acceleration/2 + a.resistance/2, reverse=True)
    #add points to the riders
    GiveWinPoints(StageNumber)
    for i in range(10):
        #timegaps. add 1 sec for each top 10, then 5 sec for next 10 each and so on
        riders[i].timegap += i
        #print(riders[i].name + " " +str( riders[i].timegap))
    for i in range(10, len(riders)-1):
        riders[i].timegap += 10 + int(i/10) * 5
        #print(riders[i].name + " " + str(riders[i].timegap))
    AssignGCPoints(StageNumber)

def GiveWinPoints(StageNumber):
    for q in range(20):
        winPoints = 0
        for i in range(7):
            winPoints += pointsSheet.cell(2 + q + i, 2).value
        winPoints/=7
        #print (riders[q].name + " " + str(winPoints))
        sheet.cell(riders[q].index, 18 + StageNumber).value = int(winPoints)

def DownHill(StageNumber):
    riders.sort(key=lambda a: a.mountain)
    selection = []
    for i in range(20):
        selection.append(riders[i])

    selection.sort(key=lambda a: 2 * a.mountain + a.sprint + a.downhill/3)
    for i in range(20):
        riders[i] = selection[i]
    GiveWinPoints(StageNumber)

    for i in range(10):
        #timegaps. add 1 sec for each top 10, then 5 sec for next 10 each and so on
        riders[i].timegap += i
        #print(riders[i].name + " " +str( riders[i].timegap))
    for i in range(10, len(riders)-1):
        riders[i].timegap += 10 + int(i/20) * 15
        #print(riders[i].name + " " + str(riders[i].timegap))
    AssignGCPoints(StageNumber)

def MTF(StageNumber):
    riders.sort(key=lambda a: 2* a.mountain + a.resistance/2, reverse=True)
    GiveWinPoints(StageNumber)
    for i in range(len(riders)-1):
        riders[i].timegap += i * 15
    AssignGCPoints(StageNumber)


def HillyITT(StageNumber):
    riders.sort(key=lambda a: a.hill + 3*a.tt + a.resistance, reverse=True)
    GiveWinPoints(StageNumber)
    for i in range(len(riders)-1):
        riders[i].timegap += i * 4
    AssignGCPoints(StageNumber)

def AssignGCPoints(StageNumber):
    riders.sort(key=lambda a: a.timegap)
    print("Giving points: Stage " + str(StageNumber))
    for i in range(20):
        GCPoints = 0
        for q in range(7):
            GCPoints += pointsSheet.cell(2 + q + i, 5).value
        GCPoints/=7
        sheet.cell(riders[i].index, 40 + StageNumber).value = int(GCPoints)

def RunTour():
    HillStage(1)
    HillStage(2)
    SprintStage(3)
    SprintStage(4)
    HillyITT(5)
    SprintStage(6)
    HillStage(7)
    DownHill(8)
    MTF(9)
    SprintStage(10)
    DownHill(11)
    SprintStage(12)
    SprintStage(13)
    HillStage(14)
    DownHill(15)
    DownHill(16)
    MTF(17)
    MTF(18)
    SprintStage(19)
    HillyITT(20)
    SprintStage(21)

RunTour()
workbook.save("/home/alexander/cycling optimiser/finalFinal.xlsx")
