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

#General project inputs framework, customized for Rwanda
#Create a new file for each country
#To be extended with more granular regional

import pandas as pd

#Dictionary set up each variable as an array with [median, -3 std range, +3 std %age]
#Site specific project Inputs

#Configuration - are these elements used in the project?
configuration = {
    "P0" : 1,
    "P1" : 1
}

usage = {

    "EMIS_allowableTransferTime" : 4, #hrs
    "allowableWebsiteLoadingTime" : 20, #seconds
    "Allowable Document Loading Time" : 60, #seconds
    "Allowable Completed Assignments Loading Time" : 10, #seconds
    "Peak Hours" : 9,
    "Size of Website" : 700, #KB
    "Size of Document" : 200, #KB
    "Google Docs Bandwidth" : 20, #kbps
    "Internet Browsing Bandwidth" : 1, #Mbps
    "Video Data Rate (480p)" : 0.59, #Mbps
    "Teacher Prep Hours" : 4 #Hours
}

Assignments = {
    "Student Prep Time" : 4, #hours
    "Teacher Research Time" : 0.25, #Hours
    "Number of Daily Assignments Per Student" : 2,
    "Student Research Time" : 1, #Hours
    "Student Assignments Time" : 2, #hours
    "Time to Grade One Assignment" : 5 #minutes, per assignment
}

Community = {
    "Fraction of Community Using School Internet" : 0.2,
    "Session Length" : 30, #mins
    "Weekly Sessions" : 2,
    "Community Access Hours" : 8, #hrs, daily
    "Contention" : 25 #number of people sharing a "slot" of bandwidth
}

LessonPlanning = {
    "Weekly Planning Time" : 5, # hrs
    "Fraction of Planning Time Browsing" : 0.2
}

Telemedicine = {
    "Annual Checkups" : 1, # well-visits
    "Illness per Year" : 2, #number of times annually that community members needs a consult
    "Consults per Illness" : 3, #average number of consults when someone gets ill - assume onset, mid-course correction, closeout
    "Consult time" : 0.17, #hrs/patient; 10 minutes per consult
    "Consult hours" : 2 #daily number of hours that doctors are available for consultation
}

EMIS = {

    #[Nominal, -3 SD %age, +3 SD %age, frequency, unit of measure]
    "adminEnrollment" : pd.Series([500,0.1,0.1,12,'School']), # Size of enrollment data`
    "adminCohort" : pd.Series([100,0.1,0.2,4,'Students']), #Class-by-class (cohort) data
    "adminBehavioral" : pd.Series([100,0.1,0.3,12,'Students']), #Disciplnary records, etc
    "adminSpecialNeeds" : pd.Series([100,0.1,1,12,'Students']), #
    "adminAdministrativeIndicators" : pd.Series([1000,0.1,0.7,4,'School']), #
    "adminFinancialData" : pd.Series([10000,0.1,0.5,12,'School']), #High level finances

    "financialBudget" : pd.Series([10000,0.3,0.3,12,'School']), #
    "financialSchool Fees" : pd.Series([100,0.2,0.2,4,'Students']), #
    "financialSupply and inventory" : pd.Series([1000,0.2,0.2,12,'School']), #

    "hrSalaries" : pd.Series([10,0.1,0.1,4,'Employees']), #
    "hrEmployee profiles" : pd.Series([100,0.1,0.1,4,'Employees']), #
    "hrProfessional development data" : pd.Series([100,0.1,0.3,12,'Teachers']), #
    "hrCertification and training data" : pd.Series([100,0.1,0.7,4,'Teachers']), #
    "hrDisciplinary records" : pd.Series([100,0.1,0.1,12,'Employees']), #

    "outcomesGrades" : pd.Series([100,0.1,1,12,'Students']), #
    "outcomesNational assessments" : pd.Series([100,0.5,1,4,'Students']), #
    "outcomesClassroom assessments" : pd.Series([1000,0.2,1,4,'Classroom']) #
}

Portal = {

    "Voter Registration" : pd.Series([1200,0.1,0.1,'Clustered',20,'Individuals']),
    "ID Renewal" : pd.Series([800,0.1,0.1,'Uniform',365,'Individuals']),
    "Annual Taxes" : pd.Series([4500,0.1,0.1,'Clustered',5,'Households']),
    "Bill payments" : pd.Series([500,0.1,0.1,'Uniform',2,'Households']),
    "Complaints and Reporting" : pd.Series([500,0.1,0.1,'Uniform',365,'Individuals']),
    "e-Petitions" : pd.Series([500,0.1,0.1,'Uniform',60,'Individuals']),
}


demo = {
    "studentTeacherRatio" : 30,
    "teacherClassroomRatio" : 1.2, #20% of teachers not teaching during a given period
    "schoolAgeFraction" : 0.354, #35% of Rwandans between ages 5-19 - https://www.populationpyramid.net/rwanda/2020/
    "schoolEnrollmentFraction" : 0.966, #96.6% of eligible Rwandans enrolled in school
    "peoplePerHousehold" : 6,
    "labor_cost_skilled" : 15, #usd/hr
    "labor_cost_regular" : 1 #usd/hr
}
