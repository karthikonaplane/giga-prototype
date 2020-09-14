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

#Pulls in raw list of schools then does the following:
#Finds all schools within n meters (input)
#Combines into a single school

#Finds number of points within a radius of the specified point

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


#import scipy.spatial as spatial
from grispy import GriSPy

def consolidateSchools(schoolData,radius,verbose):
    radius = radius/1000
    #Create empty dataframes
    #resultsDF = pd.DataFrame(columns=['pointsInRadius','nearestPoint'])


    #def computeBandwidth(lat,lon,radius):
    if(verbose):
        print('Reading.....')
    #schoolData = pd.read_excel(args.File)
    latlonArray = schoolData[['Lat', 'Lon']].to_numpy()

    #Build grid
    if(verbose):
        print('Building Grid.....')
    gsp = GriSPy(latlonArray)

    degPerKM = 0.0089#Degrees per 1 km
    upper_radii = radius * degPerKM

    numSchools = len(schoolData.index)

    dropList = []
    numberDropped = 0
    for i in range(numSchools):
        center = latlonArray[i].reshape(1,2)

        #Find all other points in latlonArray which are within upper_radii
        #from the current center point
        bubble_dist, bubble_ind = gsp.bubble_neighbors(
            center, distance_upper_bound=upper_radii
            )

        #These are the indices of schools inside the radius
        bubble_ind = np.array(bubble_ind)

        schoolsInRadius = bubble_ind.size-1

        #A bit of a hack but don't drop *multiple* schools -- only one. If more
        #than one school is found that probably means it's a high density area.

        #For later -- use multiple column matching (names etc)
        if schoolsInRadius == 1:
            numberDropped = numberDropped + 1
            #print(bubble_ind[0][0])
            #drop the data - ignore errors if
            schoolData = schoolData.drop([bubble_ind[0][0]],errors='ignore')

    #print(dropList)


    #schoolData.drop(dropList)
    schoolData = schoolData.reset_index(drop=True)
    print('NUMBER DROPPED = ', numberDropped)
    #print(schoolData.head())
    input()

    return(schoolData)
