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
import pandas as pd

import rasterio
# import rasterio.features
# import rasterio.warp

from pointsInCircle import pointsInCircle

#Set up inputs
# import argparse #For input arguments

# parser = argparse.ArgumentParser()
# parser.add_argument("-f", "--File", help="Filename for data input", action="store")
# parser.add_argument("-g", "--Geo", help="Filename for GeoTiff Pop input", action="store")
# parser.add_argument("-v", "--Verbose", help="Verbose: print intermediae outputs", action="store_true")
# args = parser.parse_args()
#
# schoolData = pd.read_excel(args.File)
# radiuskm = 10 #km


def computeSchoolCensus(schoolData,radiuskm,popTiff,verbose):

    degPerkm = 0.0089#Degrees per 10 km
    pixelResolution = 0.100 #km per pixel

    outOfCountryFlag = 0

    #Setup outputs
    results = []

    #Load Geotiff
    #dataset = rasterio.open(args.Geo)
    dataset = rasterio.open(popTiff)

    #Set up traformation matrices. [lon;lat] = [Affine] * [xpixel;ypixel]
    affine = dataset.transform
    invAffine = ~affine

    #Load in population dataset and clip values
    popData = dataset.read(1)
    popData[popData<0] = 0

    #Compute school populations

    lat = schoolData['Lat']
    lon = schoolData['Lon']

    numSchools = len(schoolData.index)

    for i in range(numSchools):
        #Find pixel in dataset where school is located
        schoolPixel = np.floor(invAffine * [lon[i], lat[i]])
        if(schoolData['Distance to Nearest School'][i] > radiuskm and schoolData['Distance to Nearest School'][i] < 200):
            radius = schoolData['Distance to Nearest School'][i]
        else:
            radius = radiuskm

        #Check if pixel is within radius of country bounds, if not snap back into the country temporarily
        if (schoolPixel[0] < radius/pixelResolution):
            schoolPixel[0] = radius/pixelResolution + 1
            outOfCountryFlag = 1

        if (schoolPixel[0] > dataset.width - radius/pixelResolution):
            schoolPixel[0] = dataset.width - radius/pixelResolution - 1
            outOfCountryFlag = 1

        if (schoolPixel[1] < radius/pixelResolution):
            schoolPixel[1] = radius/pixelResolution + 1
            outOfCountryFlag = 1

        if (schoolPixel[1] > dataset.height - radius/pixelResolution):
            schoolPixel[1] = dataset.height - radius/pixelResolution - 1
            outOfCountryFlag = 1

        #Find all pixels within given radius of school
        schoolCatchmentX, schoolCatchmentY = pointsInCircle(schoolPixel[0], schoolPixel[1],np.floor(radius/pixelResolution))

        #Extract number of people of surrounding areas

        print(i)
        catchmentPop = popData[schoolCatchmentY, schoolCatchmentX] #yes, it's Y, X not X, Y

        #Compute total population in radius of school
        totalPopulationInCatchment = np.floor(np.sum(catchmentPop)) #Since all pixels are assuming to be the same size

        #And then if the pixel was outside the country, just set the school population back to 0
        if(outOfCountryFlag == 1):
            totalPopulationInCatchment = 0
            outOfCountryFlag = 0

        results.append(totalPopulationInCatchment)

        if verbose==1:
            print(i)
            print('Total Surrounding Population:', totalPopulationInCatchment)

    resultDF = pd.DataFrame(results, columns = ['Total Surrounding Population'])
    return(resultDF)
