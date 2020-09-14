
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

#Finds number of points within a radius of the specified point

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


#import scipy.spatial as spatial
from grispy import GriSPy


#Set up inputs
# import argparse #For input arguments
#
# parser = argparse.ArgumentParser()
# parser.add_argument("-f", "--File", help="Filename for data input", action="store")
# #parser.add_argument("-v", "--Verbose", help="Verbose: print intermediae outputs", action="store_true")
# args = parser.parse_args()


def findNumberOfNeighbors(schoolData,radius,verbose):

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

    degPerKM = 0.0089#Degrees per 10 km
    upper_radii = radius * degPerKM
    n_nearest = 1

    numSchools = len(schoolData.index)

    resultsList = []
    for i in range(numSchools):
        center = latlonArray[i].reshape(1,2)

        #Find all other points in latlonArray which are within upper_radii
        #from the current center point
        bubble_dist, bubble_ind = gsp.bubble_neighbors(
            center, distance_upper_bound=upper_radii
            )

        #Compute the distance to the nearest location
        near_dist, near_ind = gsp.nearest_neighbors(center, n=n_nearest)

        bubble_ind = np.array(bubble_ind)

        #Append number of locations within certain distance, closest point
        resultsList.append([bubble_ind.size-1, float(near_dist[0]/degPerKM)])

        if i == 0 and verbose:
            print("Number of Nearby Schools", bubble_ind.size-1)
            print("Nearest School Location:",latlonArray[tuple(near_ind)])


        if(verbose):
            if(bubble_ind.size == 1):
                print("----->School Index:",i)
                print("School Location:",latlonArray[i])
                print("Number of Nearby Schools", bubble_ind.size-1)
                #print("Locations:",bubble_ind[i])
                #print("Distances:",bubble_dist[i])
                print("Nearest School Location:",latlonArray[near_ind])
                print("Nearest School Distance:",near_dist[0]/degPerKM)

        #resultsDF['pointsInRadius'][i] = bubble_ind.size-1
        #resultsDF['nearestPoint'][i] = near_dist[0]/degPerKM
    resultDF = pd.DataFrame(resultsList, columns = ['numPoints', 'nearestNeighbor'])
    #print(resultDF.head())
    return(resultDF)
