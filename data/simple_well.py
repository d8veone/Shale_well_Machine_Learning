'''
    PIPESIM Python Toolkit
     
'''

# ---------------------------------------------------------------------------
# The files that we are going to use
# ---------------------------------------------------------------------------

import os
import xlwings as xw
import pandas as pd
from enpyxll import entry_point
from pyxll import xl_macro, xl_app, xlcAlert
from sixgill.definitions import Parameters, Constants, SystemVariables, ProfileVariables
from sixgill.pipesim import Model
EXCEL_FILE = "simple_well.xlsx"
MODEL_FILE = "simple_well.pips"

# ---------------------------------------------------------------------------
# Imports and Global declarations
# ---------------------------------------------------------------------------

# Import the functions for working with Pipesim

# Import the functions for working within Excel
# and any other Python modules that we are going to use

# Locations in the Excel workbook
START = "A7"
RESULTS = "N7"
SHEET = "Production Data"

# The list of variables that we need from running the model
RESULT_VARIABLES = [SystemVariables.PRESSURE,
                    SystemVariables.TEMPERATURE,
                    SystemVariables.TOTAL_LIQUID_HOLDUP,
                    SystemVariables.REYNOLDS_NUMBER_MEAN
                    ]
PROFILE_VARIABLES = [ProfileVariables.FLOW_PATTERN_GAS_LIQUID,
                     ProfileVariables.FLOW_PATTERN_OIL_WATER,
                     ProfileVariables.SUPERFICIAL_VELOCITY_GAS,
                     ProfileVariables.SUPERFICIAL_VELOCITY_LIQUID,
                     ProfileVariables.SURFACE_TENSION_LIQUID_INSITU,
                     ProfileVariables.VISCOSITY_LIQUID_INSITU,
                     ProfileVariables.SURFACE_TENSION_LIQUID_INSITU,
                     ProfileVariables.REYNOLDS_NUMBER,
                     ProfileVariables.PRESSURE,
                     ProfileVariables.TEMPERATURE,
                     ProfileVariables.HOLDUP_FRACTION_LIQUID,
                     ProfileVariables.FROUDE_NUMBER_GAS,
                     ProfileVariables.TOTAL_DISTANCE,
                     ProfileVariables.FROUDE_NUMBER_LIQUID
                     ]


# ---------------------------------------------------------------------------
# Main code
# ---------------------------------------------------------------------------

# Figure out the model and Excel filenames
folder = os.path.dirname(__file__)
excelfile = os.path.join(folder, EXCEL_FILE)
modelfile = os.path.abspath(os.path.join(folder, MODEL_FILE))

# Open the Excel and PIPESIM model files
print("Opening Excel workbook {}".format(excelfile))
excel = xw.Book(excelfile)
datasheet = excel.sheets(SHEET)
print("Opening model {}".format(modelfile))
model = Model.open(modelfile)

# Read each line and run the network simulation
row = datasheet.range(START).row
col = datasheet.range(START).column
rescol = datasheet.range(RESULTS).column
while datasheet.cells(row, col).value:

    # Get the data for the day
    date = datasheet.cells(row, 1).value
    gas_rate = datasheet.cells(row, 2).value
    oil_rate = datasheet.cells(row, 3).value
    water_rate = datasheet.cells(row, 4).value
    press = datasheet.cells(row, 5).value
    temp = datasheet.cells(row, 6).value

    # Update the model boundary with the data
    model.tasks.networksimulation.set_conditions({
        "gas": {
            Parameters.Boundary.GASFLOWRATE: gas_rate,
            Parameters.Boundary.PRESSURE: press,
            Parameters.Boundary.TEMPERATURE: temp
        },
        "cond": {
            Parameters.Boundary.LIQUIDFLOWRATE: oil_rate,
            Parameters.Boundary.TEMPERATURE: temp
        },
        "water": {
            Parameters.Boundary.LIQUIDFLOWRATE: water_rate,
            Parameters.Boundary.TEMPERATURE: temp
        }
    })
    # model.set_values({"Choke":{Parameters.Choke.BEANSIZE:bs}})

    # Run the model
    print("Running the simulation for {} with gas={}, Oil ={}, Gas ={}, pressure={}".format(date, gas_rate, oil_rate,
                                                                                            water_rate, press))
    results = model.tasks.networksimulation.run(
        profile_variables=PROFILE_VARIABLES, system_variables=RESULT_VARIABLES)
    print(results.node)
    # print(results.profile)

    # Write out the results
    # Flat section
    datasheet.cells(
        row, rescol).value = results.profile['Sk']['FlowPatternGasLiquid'][2]  # FLAT SECTION
    datasheet.cells(
        row, rescol + 1).value = results.profile['Sk']['FroudeNumberGas'][2]  # FLAT SECTION
    datasheet.cells(
        row, rescol + 2).value = results.profile['Sk']['FroudeNumberLiquid'][2]  # FLAT SECTION
    datasheet.cells(
        row, rescol + 3).value = results.profile['Sk']['HoldupFractionLiquid'][2]  # FLAT SECTION
    datasheet.cells(
        row, rescol + 4).value = results.profile['Sk']['Pressure'][2]  # FLAT SECTION
    datasheet.cells(
        row, rescol + 5).value = results.profile['Sk']['ReynoldsNumber'][2]  # FLAT SECTION
    datasheet.cells(
        row, rescol + 6).value = results.profile['Sk']['SuperficialVelocityGas'][2]  # FLAT SECTION
    datasheet.cells(
        row, rescol + 7).value = results.profile['Sk']['SuperficialVelocityLiquid'][2]  # FLAT SECTION
    datasheet.cells(
        row, rescol + 8).value = results.profile['Sk']['SurfaceTensionLiquidInSitu'][2]  # FLAT SECTION
    datasheet.cells(
        row, rescol + 9).value = results.profile['Sk']['Temperature'][2]  # FLAT SECTION
    datasheet.cells(
        row, rescol + 10).value = results.profile['Sk']['ViscosityLiquidInSitu'][2]  # FLAT SECTION
    # Riser section
    datasheet.cells(
        row, rescol + 11).value = results.profile['Sk']['FlowPatternGasLiquid'][6]  # RISER SECTION
    datasheet.cells(
        row, rescol + 12).value = results.profile['Sk']['FroudeNumberGas'][6]  # RISER SECTION SECTION
    datasheet.cells(
        row, rescol + 13).value = results.profile['Sk']['FroudeNumberLiquid'][6]  # RISER SECTION
    datasheet.cells(
        row, rescol + 14).value = results.profile['Sk']['HoldupFractionLiquid'][6]  # RISER SECTION
    datasheet.cells(
        row, rescol + 15).value = results.profile['Sk']['Pressure'][6]  # RISER SECTION
    datasheet.cells(
        row, rescol + 16).value = results.profile['Sk']['ReynoldsNumber'][6]  # RISER SECTION
    datasheet.cells(
        row, rescol + 17).value = results.profile['Sk']['SuperficialVelocityGas'][6]  # RISER SECTION
    datasheet.cells(
        row, rescol + 18).value = results.profile['Sk']['SuperficialVelocityLiquid'][6]  # RISER SECTION
    datasheet.cells(
        row, rescol + 19).value = results.profile['Sk']['SurfaceTensionLiquidInSitu'][6]  # RISER SECTION
    datasheet.cells(
        row, rescol + 20).value = results.profile['Sk']['Temperature'][6]  # RISER SECTION
    datasheet.cells(
        row, rescol + 21).value = results.profile['Sk']['ViscosityLiquidInSitu'][6]  # RISER SECTION
    # Arrival
    datasheet.cells(
        row, rescol + 22).value = results.node[SystemVariables.PRESSURE]['Sk']
    datasheet.cells(
        row, rescol + 23).value = results.node[SystemVariables.TEMPERATURE]['Sk']

    # Move on to the next day
    row += 1

# df=pd.DataFrame(results.profile['Sk'])
# df.to_csv('df.csv')
