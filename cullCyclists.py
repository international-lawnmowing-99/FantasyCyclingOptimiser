from ast import Index
from os import truncate
from openpyxl import load_workbook
import unicodedata

#
# This gets you 9/10 of the way there. To finish up, make a new column with the list from procyclingstats sorted alphabetically and compare it to the output of
# chosenOnes to see which names were entered differently in the pcm game (i.e. Sergio Henao vs Sergio Luis Henao)
#




from openpyxl.worksheet import worksheet
workbook = load_workbook(filename="cyclists.xlsx")
#print(workbook.sheetnames)
sheet = workbook.active


namesText = open("selectedRiders.txt", "r")
textLines = namesText.read().splitlines()

rows, cols = (2,len(textLines))
arr = [[0 for i in range(cols)] for j in range(rows)]


for i in range(cols):
    splitLine = textLines[i].split()
    #print(splitLine)
    numberOfStrings = len(splitLine)
    firstName = ""
    lastName = ""
    #print(firstName + " " + str(numberOfSplits))
    count = 0
    while count < numberOfStrings:
        if unicodedata.normalize('NFD', splitLine[count]).encode('ascii', 'ignore').upper().decode('ascii', 'ignore') == unicodedata.normalize('NFD', splitLine[count]).encode('ascii', 'ignore').decode('ascii', 'ignore'):
            # it is all caps, therefore lastName
            if lastName == "":
                lastName += unicodedata.normalize('NFD', splitLine[count]).encode('ascii', 'ignore').lower().decode('ascii', 'ignore')
            else:
                lastName += " "
                lastName += unicodedata.normalize('NFD', splitLine[count]).encode('ascii', 'ignore').lower().decode('ascii', 'ignore')
        else:
            if firstName == "":
                firstName += unicodedata.normalize('NFD', splitLine[count]).encode('ascii', 'ignore').lower().decode('ascii', 'ignore')
            else:
                firstName += " "
                firstName += unicodedata.normalize('NFD', splitLine[count]).encode('ascii', 'ignore').lower().decode('ascii', 'ignore')
        count += 1

    print(firstName + " ||| " + lastName)
    arr[0][i] = firstName
    arr[1][i] = lastName

deletionRows = []
selectionCount = 0
print ("rots " + str(sheet.max_row))
for i in range(2, sheet.max_row + 1):
    lastName = unicodedata.normalize('NFD', sheet.cell(i,1).value).encode('ascii', 'ignore').lower().decode('ascii', 'ignore')
    firstName = unicodedata.normalize('NFD', sheet.cell(i,2).value).encode('ascii', 'ignore').lower().decode('ascii', 'ignore')

    print(str(i) + " Testing rider, sheet: " + firstName +" "+ lastName)

    if (arr[0].__contains__(firstName)):
        matchingFirstNames = [q for q, x in enumerate(arr[0]) if x == firstName]
        foundMatch = False

        for indix in matchingFirstNames:
            print(str(indix) + " " + arr[1][indix])
            if arr[1][indix] == lastName:
                foundMatch = True
                print("Last Name found at: " + str(indix) + ", " + arr[1][indix])

        if foundMatch:
            selectionCount+=1
            print(str(selectionCount)+ " SELECTED " + firstName + " " + lastName)

        else:
            print (" Second name no match: " + firstName + " " + lastName)
            deletionRows.append(i)

    else:
        print("First name not found: " + firstName + " " + lastName)
        deletionRows.append(i)


def reverseCombiner(rowList):
    # Don't do anything for empty list. Otherwise,
    # make a copy and sort.

    if len(rowList) == 0: return []
    sortedList = rowList[:]
    sortedList.sort()

    # Init, empty tuple, use first item for previous and
    # first in this run.

    tupleList = []
    firstItem = sortedList[0]
    prevItem = sortedList[0]

    # Process all other items in order.

    for item in sortedList[1:]:
        # If start of new run, add tuple and use new first-in-run.

        if item != prevItem + 1:
            tupleList = [(firstItem, prevItem + 1 - firstItem)] + tupleList
            firstItem = item

        # Regardless, current becomes previous for next loop.

        prevItem = item

    # Finish off the final run and return tuple list.

    tupleList = [(firstItem, prevItem + 1 - firstItem)] + tupleList
    return tupleList


tuples = reverseCombiner(deletionRows)
for tuple in tuples:
    sheet.delete_rows(tuple[0  ], tuple[1])

workbook.save('theChosenOnes.xlsx')


def new_func(workbook, sheet):
    if  sheet.cell(2,1).value == "Pogacar":
        sheet.insert_rows(0,2)
        workbook.save('theChosenOnes.xlsx')
        print("writing")
    else:
        print("not writing")
        print(sheet['B1'])
        print (sheet.cell(2,1).value)
