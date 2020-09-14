# /*
#  * Copyright (C) 2020 ACTUAL Systems, Inc.
#  *
#  * http://www.actualhq.com
#  *
#  * In collaboration with UNICEF/Giga: https://gigaconnect.org
#  *
#  * Licensed under the Apache License, Version 2.0 (the "License");
#  * you may not use this file except in compliance with the License.
#  * You may obtain a copy of the License at
#  *
#  * http://www.apache.org/licenses/LICENSE-2.0
#  *
#  * Unless required by applicable law or agreed to in writing, software
#  * distributed under the License is distributed on an "AS IS" BASIS,
#  * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  * See the License for the specific language governing permissions and
#  * limitations under the License.
#  */


def pause():
    programPause = input("Press the <ENTER> key to continue...")


import argparse #For input arguments

import sys
import io
sys.path.insert(0, "./")

import numpy as np
import pandas as pd
from computeBandwidth import computeBandwidth
from findNumberOfNeighbors import findNumberOfNeighbors
from computeSchoolCensus import computeSchoolCensus
from computeCosts import computeCosts
from consolidateSchools import consolidateSchools
import time

#Analysis Config
sensitivity = 0
clipping = 0

#Set up inputs
parser = argparse.ArgumentParser()
parser.add_argument("-c", "--Country", help="Country for Analysis", action="store")
args = parser.parse_args()

#Import School DataFrame

#country = 'Kenya'
#country = 'Sierra Leone'
pjDefault = 1
if args.Country == 'Honduras':
    schoolDataPath = 'Honduras Data/HN_School_DN_2G_3G_4G.xlsx'
    popDataPath = 'Honduras Data/hnd_ppp_2020_UNadj.tif'
    import projectInputsHonduras as pjIn
    pjDefault = 0

if args.Country == 'Rwanda':
    schoolDataPath = 'Rwanda Data/RW_connectivity_GIGA_GSMA_DistanceNodes.xlsx'
    popDataPath = 'Rwanda Data/rwa_ppp_2020_UNadj.tif'
    import projectInputsRwanda as pjIn
    pjDefault = 0


if args.Country == 'Kenya':
    schoolDataPath = 'Kenya Data/Primary Schools list  GPS Coordinates 2020_Tusome Data_14Feb2020_ITU.xlsx'
    popDataPath = 'Kenya Data/ken_ppp_2020_UNadj.tif'

if args.Country == 'Sierra Leone':
    schoolDataPath = 'Sierra Leone Data/sl_school_connectivity.xlsx'
    popDataPath = 'Sierra Leone Data/sle_ppp_2020_UNadj.tif'

print("Country:", args.Country)
print("Loading from file", schoolDataPath)
schoolData = pd.read_excel(schoolDataPath)

#Add columns to DF for computed values

schoolData['Number of Pupils'] = ''
schoolData['Number of Teachers'] = ''
schoolData['Number of Classrooms'] = ''
schoolData['Schools Within 10 km'] = ''
schoolData['Schools Within 1 km'] = ''
schoolData['Distance to Nearest School'] = ''
schoolData['Population Within 1 km'] = ''
schoolData['Population Within 10 km'] = ''
schoolData['Local Population'] = ''
schoolData['Local Households'] = ''
schoolData['Bandwidth'] = ''
schoolData['Overnight Comms Cost'] = ''
schoolData['Annual Comms Cost'] = ''
schoolData['Overnight Power Cost'] = ''
schoolData['Annual Power Cost'] = ''
schoolData['Overnight Cost'] = ''
schoolData['Annual Cost'] = ''
schoolData['Tech'] = ''

#Import project global data
print("Importing Project Config")
if (pjDefault == 1):
    import projectInputs as pjIn
import techInputs as techIn
dictionaries = ["configuration","usage", "EMIS"]
techTypes = ['fiber','cell2G','cell3G','cell4G','WISP','satellite']

#=======Drop schools that are within range of each other (assume same school building)
radiusSameSchool = 10 #m
schoolData = consolidateSchools(schoolData,radiusSameSchool,1)

#=======Compute population of each school
#Compute number of schools within a given radius of each school
print("Computing populations for each school")
radius = 10 #km
verbose_schooldata = 0
nearestSchoolData = findNumberOfNeighbors(schoolData,radius,verbose_schooldata)
schoolData['Schools Within 10 km'] = nearestSchoolData['numPoints']
schoolData['Distance to Nearest School'] = nearestSchoolData['nearestNeighbor']


#Compute population around school
verbose_census = 0

#Figure students in each school
studentPopRatio = pjIn.demo['schoolAgeFraction'] * pjIn.demo['schoolEnrollmentFraction']

if 'num_students' in schoolData.columns:
    schoolData['Number of Pupils'] = schoolData['num_students']
else:
    schoolData['Population Within 10 km'] = computeSchoolCensus(schoolData,radius,popDataPath,verbose_census)
    schoolData['Number of Pupils'] = np.ceil(studentPopRatio * schoolData['Population Within 10 km'] /(schoolData['Schools Within 10 km']+1))

schoolData['Number of Teachers'] = np.ceil(schoolData['Number of Pupils']/pjIn.demo['studentTeacherRatio'])

#Edge Cases
schoolData['Number of Teachers'][schoolData['Number of Teachers'] < 1] = 1 #Should be at least 1 teacher....
schoolData['Number of Teachers'][schoolData['Number of Pupils'] == 0] = 0 #Unless there are no students

schoolData['Number of Classrooms'] = np.ceil(schoolData['Number of Teachers'] * pjIn.demo['teacherClassroomRatio'])

print(schoolData['Number of Pupils'].describe())
print(schoolData['Number of Teachers'].describe())


#Compute local population (within 1 km) who will come to the school for internet
radiusLocalInternet = 1 #km
verbose_localpop = 0
nearestSchoolInternetData = findNumberOfNeighbors(schoolData,radiusLocalInternet,verbose_localpop)
schoolData['Schools Within 1 km'] = np.maximum(1,nearestSchoolInternetData['numPoints'])
#Divide population among local schools to not overcount bandwidth needs
schoolData['Population Within 1 km'] = computeSchoolCensus(schoolData,radiusLocalInternet,popDataPath,verbose_localpop)
schoolData['Local Population'] = schoolData['Population Within 1 km']/schoolData['Schools Within 1 km']
schoolData['Local Households'] = np.floor(schoolData['Local Population']/pjIn.demo['peoplePerHousehold'])

print(schoolData['Local Population'].describe())

#=======Compute Bandwidth
print("Computing Bandwidth")

for schoolIndex in schoolData.index:
#for schoolIndex in range(10):
    print("Computing BW for:",schoolIndex)
    verbose = 0
    finalTechSelection = 0
    result = []
    specificSchoolData = schoolData.iloc[schoolIndex]

    #Compute bandwidth
    BWNom = computeBandwidth(specificSchoolData,pjIn,verbose)
    schoolData['Bandwidth'][schoolIndex] = BWNom

#=======Figure out correct tech option -- to revise later
schoolData['Tech'][((schoolData['Bandwidth'] < techIn.cell4G['speed']) &
                    (schoolData['Tech'] == '') &
                    (schoolData['Type of Cell Coverage'] == '4G'))] = 'cell4G'

schoolData['Tech'][(schoolData['Distance to Nearest Fiber'] < 10) &
                    (schoolData['Tech'] == '')] = 'fiber'

schoolData['Tech'][((schoolData['Distance to Nearest Fiber'] >= 10) &
                    (schoolData['Distance to Nearest Fiber'] < 20))] = 'WISP'

schoolData['Tech'][((schoolData['Bandwidth'] < techIn.cell2G['speed']) &
                    (schoolData['Tech'] == '') &
                    (schoolData['Type of Cell Coverage'] == '2G'))] = 'cell2G'

schoolData['Tech'][((schoolData['Bandwidth'] < techIn.cell3G['speed']) &
                    (schoolData['Tech'] == '') &
                    (schoolData['Type of Cell Coverage'] == '3G'))] = 'cell3G'



schoolData['Tech'][(schoolData['Tech'] == '')] = 'satellite'

print(schoolData['Tech'].describe())

#=======Compute Costs

verbose_costs = 1
schoolData['Overnight Comms Cost'], schoolData['Annual Comms Cost'], schoolData['Overnight Power Cost'], schoolData['Annual Power Cost'] = computeCosts(schoolData,pjIn,techIn,techTypes,verbose_costs)
schoolData['Overnight Cost'] = schoolData['Overnight Comms Cost'] + schoolData['Overnight Power Cost']
schoolData['Annual Cost'] = schoolData['Annual Comms Cost'] + schoolData['Annual Power Cost']

#print(schoolData['Overnight Cost'])

schoolData.to_csv("school_output.csv")
    # if sensitivity == 1:
    #     verbose = 0
    #
    #     for dicts in dictionaries:
    #         for key, value in getattr(pjIn,dicts).items():
    #             if isinstance(value, list):
    #
    #                 ##########
    #                 #Run for nominal
    #                 BWNom = computePerformance(specificSchoolData,pjIn,verbose)
    #
    #
    #                 ##########
    #                 #Run for max input value
    #                 holdvalue = value[0]
    #                 value[0] = holdvalue * (1 + value[2])
    #                 BWMaxInput = computePerformance(specificSchoolData,pjIn,verbose)
    #
    #                 ##########
    #                 #Run for min input value
    #                 value[0] = holdvalue * (1 - value[1])
    #
    #                 #Inputs should not be negative - clip and store
    #                 if value[0] < 0:
    #                     value[0] = 0
    #
    #                 BWMinInput = computePerformance(specificSchoolData,pjIn,verbose)
    #
    #                 #Return value from placeholder
    #                 value[0] = holdvalue
    #
    #
    #
    #                 ##########Computation. Handle nan (ex. if project returns nothing)
    #
    #                 if np.isnan(BWMinInput):
    #                     BWMax = BWMaxInput
    #                     BWMin = -1
    #                 else:
    #                     BWMax = np.maximum(BWMaxInput,BWMinInput)
    #                     BWMin = np.minimum(BWMaxInput,BWMinInput)
    #
    #
    #                 result = result + [key,BWNom,BWMin,BWMax,(BWMax-BWMin)]
    #                 #resultDF.append(result)
    #     result = np.reshape(result,(-1,5))
    #
    #
    #     resultDF = pd.DataFrame(result, columns=['Variable','BWNom','BWMin','BWMax','BWRange'])
    #     resultDF['BWNom'] = pd.to_numeric(resultDF['BWNom'], errors='ignore')
    #     resultDF['BWMin'] = pd.to_numeric(resultDF['BWMin'], errors='ignore')
    #     resultDF['BWMax'] = pd.to_numeric(resultDF['BWMax'], errors='ignore')
    #     resultDF['BWRange'] = pd.to_numeric(resultDF['BWRange'], errors='ignore')
    #     pd.options.display.float_format = '{:.2f}'.format
    #
    #
    #     resultDF = resultDF.sort_values(by=['BWRange'],ascending=False)
    #     #print(resultDF)



        #Plot
        #
        # Y = np.arange(len(resultDF.index))
        # range = list(resultDF["BWRange"].astype(np.float))
        # range = np.array(range)
        # start = list(resultDF["BWMin"].astype(np.float))
        # start = np.array(start)
        #
        # plt.barh(Y,range, left=start)
        #plt.show()
