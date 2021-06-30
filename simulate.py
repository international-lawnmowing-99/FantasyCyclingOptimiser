from rider import Rider
from openpyxl import load_workbook
import unicodedata
from openpyxl.worksheet import worksheet
workbook = load_workbook(filename="/home/alexander/cycling optimiser/finalFinal.xlsx")
sheet = workbook["DYN_cyclist"]
pointsSheet = workbook["PointsSheet"]

NON_NFKD_MAP = {u'\u0181': u'B', u'\u1d81': u'd', u'\u1d85': u'l', u'\u1d89': u'r', u'\u028b': u'v', u'\u1d8d': u'x', u'\u1d83': u'g', u'\u0191': u'F', u'\u0199': u'k', u'\u019d': u'N', u'\u0220': u'N', u'\u01a5': u'p', u'\u0224': u'Z', u'\u0126': u'H', u'\u01ad': u't', u'\u01b5': u'Z', u'\u0234': u'l', u'\u023c': u'c', u'\u0240': u'z', u'\u0142': u'l', u'\u0244': u'U', u'\u2c60': u'L', u'\u0248': u'J', u'\ua74a': u'O', u'\u024c': u'R', u'\ua752': u'P', u'\ua756': u'Q', u'\ua75a': u'R', u'\ua75e': u'V', u'\u0260': u'g', u'\u01e5': u'g', u'\u2c64': u'R', u'\u0166': u'T', u'\u0268': u'i', u'\u2c66': u't', u'\u026c': u'l', u'\u1d6e': u'f', u'\u1d87': u'n', u'\u1d72': u'r', u'\u2c74': u'v', u'\u1d76': u'z', u'\u2c78': u'e', u'\u027c': u'r', u'\u1eff': u'y', u'\ua741': u'k', u'\u0182': u'B', u'\u1d86': u'm', u'\u0288': u't', u'\u018a': u'D', u'\u1d8e': u'z', u'\u0111': u'd', u'\u0290': u'z', u'\u0192': u'f', u'\u1d96': u'i', u'\u019a': u'l', u'\u019e': u'n', u'\u1d88': u'p', u'\u02a0': u'q', u'\u01ae': u'T', u'\u01b2': u'V', u'\u01b6': u'z', u'\u023b': u'C', u'\u023f': u's', u'\u0141': u'L', u'\u0243': u'B', u'\ua745': u'k', u'\u0247': u'e', u'\ua749': u'l', u'\u024b': u'q', u'\ua74d': u'o', u'\u024f': u'y', u'\ua751': u'p', u'\u0253': u'b', u'\ua755': u'p', u'\u0257': u'd', u'\ua759': u'q', u'\xd8': u'O', u'\u2c63': u'P', u'\u2c67': u'H', u'\u026b': u'l', u'\u1d6d': u'd', u'\u1d71': u'p', u'\u0273': u'n', u'\u1d75': u't', u'\u1d91': u'd', u'\xf8': u'o', u'\u2c7e': u'S', u'\u1d7d': u'p', u'\u2c7f': u'Z', u'\u0183': u'b', u'\u0187': u'C', u'\u1d80': u'b', u'\u0289': u'u', u'\u018b': u'D', u'\u1d8f': u'a', u'\u0291': u'z', u'\u0110': u'D', u'\u0193': u'G', u'\u1d82': u'f', u'\u0197': u'I', u'\u029d': u'j', u'\u019f': u'O', u'\u2c6c': u'z', u'\u01ab': u't', u'\u01b3': u'Y', u'\u0236': u't', u'\u023a': u'A', u'\u023e': u'T', u'\ua740': u'K', u'\u1d8a': u's', u'\ua744': u'K', u'\u0246': u'E', u'\ua748': u'L', u'\ua74c': u'O', u'\u024e': u'Y', u'\ua750': u'P', u'\ua754': u'P', u'\u0256': u'd', u'\ua758': u'Q', u'\u2c62': u'L', u'\u0266': u'h', u'\u2c73': u'w', u'\u2c6a': u'k', u'\u1d6c': u'b', u'\u2c6e': u'M', u'\u1d70': u'n', u'\u0272': u'n', u'\u1d92': u'e', u'\u1d74': u's', u'\u2c7a': u'o', u'\u2c6b': u'Z', u'\u027e': u'r', u'\u0180': u'b', u'\u0282': u's', u'\u1d84': u'k', u'\u0188': u'c', u'\u018c': u'd', u'\ua742': u'K', u'\u1d99': u'u', u'\u0198': u'K', u'\u1d8c': u'v', u'\u0221': u'd', u'\u2c71': u'v', u'\u0225': u'z', u'\u01a4': u'P', u'\u0127': u'h', u'\u01ac': u'T', u'\u0235': u'n', u'\u01b4': u'y', u'\u2c72': u'W', u'\u023d': u'L', u'\ua743': u'k', u'\u0249': u'j', u'\ua74b': u'o', u'\u024d': u'r', u'\ua753': u'p', u'\u0255': u'c', u'\ua757': u'q', u'\u2c68': u'h', u'\ua75b': u'r', u'\ua75f': u'v', u'\u2c61': u'l', u'\u2c65': u'a', u'\u01e4': u'G', u'\u0167': u't', u'\u2c69': u'K', u'\u026d': u'l', u'\u1d6f': u'm', u'\u0271': u'm', u'\u1d73': u'r', u'\u027d': u'r', u'\u1efe': u'Y'}

def deaccent(name):
    # Convert accented chars to their non-accented equivalent.
    # e.g.: Polynésie Française -> Polynesie Francaise
    if not isinstance(name, str):
        name = str(name)

    return ''.join(NON_NFKD_MAP[c] if c in NON_NFKD_MAP else c \
                   for part in unicodedata.normalize('NFKD', name) for c in part
                   if unicodedata.category(part) != 'Mn')

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
