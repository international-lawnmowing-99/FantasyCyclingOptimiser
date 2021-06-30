from pulp import *
import openpyxl
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)

cwd = os.getcwd()  # Get the current working directory (cwd)
files = os.listdir(cwd)  # Get all the files in that directory
print("Files in %r: %s" % (cwd, files))

sheet = openpyxl.load_workbook("/home/alexander/cycling optimiser/finalFinal.xlsx", data_only=True)['DYN_cyclist']

model = LpProblem("Cycling_Optimiser", LpMaximize)

function = ""
costConstraint = ""
sprinterContraint = ""
climberConstraint = ""
unclassedConstrant = ""
numberOfRidersConstraint = ""
variables = []
for i in range(184):
    print(str(i))
    variable = LpVariable(str(i), 0,1,LpInteger)
    variables.append(variable)
    print(type(sheet.cell(i+2, 16).value))
    print(sheet.cell(i+2, 16).value)


    function +=  sheet.cell(i+2, 63).value * variable
    costConstraint += int(sheet.cell(i+2, 16).value) * variable
    numberOfRidersConstraint += variable

model += function
model += (costConstraint <= 100)
model += (numberOfRidersConstraint == 8)
print(type(function))



optimization_result = model.solve()

assert optimization_result == LpStatusOptimal
print("Status:", LpStatus[model.status])
print("Optimal Solution to the problem: ", value(model.objective))
print ("Individual decision_variables: ")
for v in model.variables():
    if v.varValue == 1:
        print(sheet.cell(int(v.name) + 2, 1).value, " ", sheet.cell(int(v.name) + 2, 2).value)
