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

import sys
import io
# sys.path.insert(0, './')

import numpy as np
import pandas as pd
import pprint

import matplotlib.pyplot as plt


def computeBandwidth(schoolData,pjIn,verbose):

    if verbose == 0:
        text_trap = io.StringIO()
        sys.stdout = text_trap

    #Setup dictionaries for computation
    EMISdatasize = {}
    bandwidth = {}
    schoolParameters = {}

    #Conversion Constants
    secPerHr = 3600
    secPerMin = 60
    KBperMb = 125 #kiloBYTES per megabit
    kbperMb = 1024 #kiloBITS per megabit

    #Dataframes
    EMIScol = ['nom','-3SD','+3SD','Frequency','Unit of Measure']
    dfEMIS = pd.DataFrame.from_dict(pjIn.EMIS, orient='index')
    dfEMIS.columns = EMIScol

    Portalcol = ['nom','-3SD','+3SD','Usage Pattern','Time Period (days)','Unit of Measure']
    dfPortal = pd.DataFrame.from_dict(pjIn.Portal, orient='index')
    dfPortal.columns = Portalcol

    dfAssignments = pd.DataFrame()

    #---------------Load in school configuration

    name = schoolData['School Name']
    students = schoolData['Number of Pupils']
    teachers = schoolData['Number of Teachers']
    classrooms = schoolData['Number of Classrooms']
    lat = schoolData['Lat']
    lon = schoolData['Lon']
    fiberDistance = schoolData['Distance to Nearest Fiber']
    cellCoverage = schoolData['Type of Cell Coverage']
    school = students/students
    employees = max(2,np.floor(teachers/10))

    individuals = schoolData['Local Population']
    households = schoolData['Local Households']

    print('=============================')
    print('---->School:',name)

    #Dict of roles
    roles = ({'Teachers' : teachers, 'Classroom' : classrooms,
              'Students' : students, 'School' : school,
              'Employees' : employees, 'Individuals' : individuals,
              'Households' : households})


    #-To Do - Make Dynamic
    #print(pjIn.configuration)
    if(pjIn.configuration['P0']):
    #===========EMIS Data
        dfEMIS['Number of Agents'] = dfEMIS['Unit of Measure'].map(roles)
        dfEMIS['Data Size'] = dfEMIS['nom'] * dfEMIS['Number of Agents']
        bandwidth['EMIS'] = (np.max(dfEMIS.groupby('Frequency')['Data Size'].sum()/
                            (pjIn.usage['EMIS_allowableTransferTime']*secPerHr))/KBperMb)

        #print(dfEMIS)

        #===========Portal Data
        dfPortal['Number of Agents'] = dfPortal['Unit of Measure'].map(roles)
        dfPortal['Sessions Per Day'] = dfPortal['Number of Agents']/dfPortal['Time Period (days)']
        dfPortal['Concurrent Sessions'] = dfPortal['Sessions Per Day']/pjIn.usage['Peak Hours']
        #print(dfPortal)
        bandwidth['Portal'] = (np.maximum(pjIn.usage['Internet Browsing Bandwidth'],
                                ((dfPortal['nom'] * dfPortal['Concurrent Sessions']/pjIn.usage['allowableWebsiteLoadingTime']/pjIn.Community['Contention'])/KBperMb).sum()))

    if(pjIn.configuration['P1']):

        #============Assignments
        dfAssignments['Bandwidth'] = ""
        dfAssignments.loc['Creating Assigments'] = ([teachers * (pjIn.Assignments['Teacher Research Time']/pjIn.usage['Teacher Prep Hours']) *
                            pjIn.usage['Size of Website']/
                            pjIn.usage['allowableWebsiteLoadingTime']/
                            KBperMb])
        dfAssignments.loc['Accessing Assigments'] = ([(students * pjIn.Assignments['Number of Daily Assignments Per Student'] /
                       (secPerHr*pjIn.Assignments['Student Prep Time'])) * pjIn.usage['Size of Document']/
                            KBperMb])

        dfAssignments.loc['Performing Research'] = ([students * pjIn.Assignments['Student Research Time']/pjIn.Assignments['Student Prep Time'] *
                                                pjIn.usage['Size of Website']/
                                                pjIn.usage['allowableWebsiteLoadingTime']/KBperMb])

        dfAssignments.loc['Completing Assignments'] = ([students * pjIn.Assignments['Student Assignments Time']/pjIn.Assignments['Student Prep Time'] *
                                                    pjIn.usage['Google Docs Bandwidth']/kbperMb])

        dfAssignments.loc['Grading Assignments'] = ([teachers * ((pjIn.usage['Size of Document']/pjIn.usage['Allowable Completed Assignments Loading Time'] * 8) +
                                                    pjIn.usage['Google Docs Bandwidth'])/kbperMb])


        bandwidth['Assignments'] = dfAssignments['Bandwidth'].sum()


        #============Recorded Instructional Clips
        bandwidth['Instructional Video'] = (classrooms * pjIn.usage['Video Data Rate (480p)'])

        #============Telemedicine Consultations
        bandwidth['Telemedicine'] = (individuals * pjIn.usage['Video Data Rate (480p)'] *
                                     (pjIn.Telemedicine['Annual Checkups'] + (pjIn.Telemedicine['Illness per Year']*pjIn.Telemedicine['Consults per Illness']))/365 *
                                     (pjIn.Telemedicine['Consult time']/pjIn.Telemedicine['Consult hours']))


        #============On-premise community internet access
        bandwidth['Community Access'] = (np.maximum(pjIn.usage['Internet Browsing Bandwidth'],
                                                    (individuals * pjIn.Community['Fraction of Community Using School Internet'] *
                                                    pjIn.Community['Weekly Sessions']/7 * pjIn.Community['Session Length']/60 /
                                                    pjIn.Community['Community Access Hours'] * pjIn.usage['Internet Browsing Bandwidth'] /
                                                    pjIn.Community['Contention'])
                                            ))

        #============Lesson Planning
        bandwidth['Lesson Planning'] = (teachers * pjIn.LessonPlanning['Weekly Planning Time']/5 *
                                        pjIn.LessonPlanning['Fraction of Planning Time Browsing'] /
                                        pjIn.usage['Teacher Prep Hours'] *
                                        pjIn.usage['Internet Browsing Bandwidth'])

    print('Bandwidth Breakdown:',bandwidth)
    BW = sum(bandwidth.values())
    print("TOTAL SCHOOL BANDWIDTH:","%.2f" % BW,"Mbps")


    #Should be max of peak and off-peak

    if verbose == 0:
        sys.stdout = sys.__stdout__



    return(BW)
