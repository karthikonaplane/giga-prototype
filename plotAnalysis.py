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

#Create new lines in "args.Country ==" section for each new country
#Can also adjust to input filenames from command line, but cleaner
#to define inside the file

def pause():
    programPause = input("Press the <ENTER> key to continue...")

#
# import sys
# import io
# sys.path.insert(0, "./")

import argparse #For input arguments


import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import altair as alt
from vega_datasets import data
import geopandas
import matplotlib.lines as mlines


from computeCosts import computeCosts

# Say, "the default sans-serif font is COMIC SANS"
matplotlib.rcParams['font.sans-serif'] = "Averta"
# Then, "ALWAYS use sans-serif fonts"
matplotlib.rcParams['font.family'] = "sans-serif"


#Argument Parser
parser = argparse.ArgumentParser()
parser.add_argument("-c", "--Country", help="Country for Analysis", action="store")
args = parser.parse_args()

#Load data

if args.Country == 'Kenya':
    #schoolCompletedAnalysis = 'Kenya Outputs/April 1 Proto - school_output - P0 and P1.csv'
    #schoolCompletedAnalysis = './school_output.csv'
    schoolCompletedAnalysis = 'Kenya Outputs/Kenya - P0 and P1 - Sept 9 - 50m exclusion - school_output.csv'
    country = geopandas.read_file('Kenya Data/ke_district_boundaries.shp')

if args.Country == 'Sierra Leone':
    country = geopandas.read_file('Sierra Leone Data/sle_admbnda_adm0_1m_gov_ocha_20161017/sle_admbnda_adm0_1m_gov_ocha_20161017.shp')
    #schoolCompletedAnalysis = 'Sierra Leone Outputs/school_output - EMIS only.csv'
    #schoolCompletedAnalysis = 'Sierra Leone Outputs/school_output - P0 and P1 - Prioritize 4G.csv'
    #schoolCompletedAnalysis = './school_output.csv'
    schoolCompletedAnalysis = 'Sierra Leone Outputs/Sierra Leone - P0 and P1 - September 0 with 50m exclusion - school_output.csv'

if args.Country == 'Honduras':
    country = geopandas.read_file('Honduras Data/hnd_admbnda_adm0_sinit_20161005/hnd_admbnda_adm0_sinit_20161005.shp')
    #schoolCompletedAnalysis = 'Honduras Outputs/Honduras-July 14 2020-P0 and P1.csv'
    schoolCompletedAnalysis = 'Honduras Outputs/Honduras - P0 and P1 - September 8- 50m exclusion - school_output.csv'

if args.Country == 'Rwanda':
    country = geopandas.read_file('Rwanda Data/rwa_adm_2006_nisr_wgs1984_20181002_shp/rwa_adm0_2006_NISR_WGS1984_20181002.shp')
    #schoolCompletedAnalysis = 'Rwanda Outputs/Rwanda - July 13 2020 - P0 and P1.csv'
    schoolCompletedAnalysis = 'Rwanda Outputs/Rwanda - P0 and P1 - September 8 - 50 m exclusion - school_output.csv'

print("Loading from file", schoolCompletedAnalysis)
schoolData = pd.read_csv(schoolCompletedAnalysis)
color_dict = { 'fiber':'Black', 'WISP':'Purple', 'satellite':'Orange', 'cell2G':'Yellow','cell3G':'green','cell4G':'red' }

#Location of Schools
country.plot(color='#b8c9d9')
plt.scatter(schoolData['Lon'],schoolData['Lat'],
            s=1,c=schoolData['Distance to Nearest Fiber'],cmap='hot')
plt.colorbar()
plt.axis('off')
plt.title('School locations, coded by distance to nearest fiber (km)')

plt.show()

#Histogram of distance to fiber
bins = np.arange(0,100,10)
xlabels = bins[1:].astype(str)
xlabels[-1] += '+'

fig, fiberdisthist = plt.subplots()
fiberdisthist.hist(np.clip(schoolData['Distance to Nearest Fiber'],bins[0],bins[-1]),bins=bins,
            rwidth=0.99, color='#607c8e')
fiberdisthist.set_ylabel('School Count')
fiberdisthist.set_xlabel('Distance to nearest fiber (km)')
fiberdisthist.set_title('Distribution of school proximity to nearest fiber (km)')
plt.xticks(ticks=bins,labels=xlabels)
plt.tight_layout()
plt.show()

#School locations by technology type

country.plot(color='#b8c9d9')
plt.scatter(schoolData['Lon'],schoolData['Lat'],
            s=1,c=[color_dict[i] for i in schoolData['Tech']])
plt.title('School locations, color coded by connection type')

print(schoolData['Tech'].describe)

blackdot = mlines.Line2D([], [], color='black', marker='.', linestyle='None',
                          markersize=4, label='Fiber')
purpledot = mlines.Line2D([], [], color='Orange', marker='.', linestyle='None',
                          markersize=4, label='Satellite')
orangedot = mlines.Line2D([], [], color='purple', marker='.', linestyle='None',
                          markersize=4, label='WISP')
yellowdot = mlines.Line2D([], [], color='yellow', marker='.', linestyle='None',
                          markersize=4, label='2G')
greendot = mlines.Line2D([], [], color='green', marker='.', linestyle='None',
                          markersize=4, label='3G')
reddot = mlines.Line2D([], [], color='red', marker='.', linestyle='None',
                          markersize=4, label='4G')


plt.legend(handles=[blackdot,orangedot,purpledot, yellowdot, greendot, reddot])
plt.axis('off')

plt.show()


#Histogram of bandwidths
bins = np.arange(0,100,10)
#bins = np.arange(0,1,.01)
xlabels = bins[0:].astype(str)
xlabels[-1] += '+'


fig, bwhist = plt.subplots()
bwhist.hist(np.clip(schoolData['Bandwidth'],bins[0],bins[-1]),bins=bins,
            rwidth=0.99, color='#607c8e')
bwhist.set_ylabel('School Count')
bwhist.set_xlabel('Bandwidth (Mbps)')
bwhist.set_title('Distribution of school bandwidth requirements')
plt.xticks(ticks=bins,labels=xlabels)

plt.tight_layout()
plt.show()

#Pareto
#
# schoolData = schoolData.sort_values(by='Bandwidth',ascending=False)
# schoolData['cumBW'] = schoolData['Bandwidth'].cumsum()/schoolData['Bandwidth'].sum()*100
#
# fig, bwPareto = plt.subplots()
# bwPareto.plot(schoolData['cumBW'])
# plt.show()

#Histogram of Technology Choices
fig, techHist = plt.subplots()
techHist.hist(schoolData['Tech'],
            rwidth=0.99, color='#607c8e')
plt.show()
print(schoolData['Bandwidth'].describe())

#
# #Plot of school locations with distance from fiber
# url_geojson = 'kenyan-counties.geojson'
# data_geojson_remote = alt.Data(url=url_geojson, format=alt.DataFormat(property='features',type='json'))
#
# background = alt.Chart(data_geojson_remote).mark_geoshape(
#     fill='lightgray',
#     stroke='white'
# ).properties(
#     width=800,
#     height=600
# )
#
# mapFiber = alt.Chart(schoolData).mark_circle(size=4).encode(
#     latitude='Lat',
#     longitude='Lon',
#     color=alt.Color('Distance to Nearest Fiber',scale=alt.Scale(scheme='darkblue'))
# ).properties(
#     height=600,
#     width=800,
#     title='Map of Schools and Distance to Nearest Fiber'
# )
# mapFiber.configure_title(
#     fontSize=20,
#     font='Averta',
#     color='gray'
# )
#
# MapToPlot = mapFiber + background
# background.serve()
#
# #Plot of school locations with tech options
# # fig, maplocs = plt.subplots()
# # plt.scatter(schoolData['Lon'],schoolData['Lat'], c=schoolData['Tech'])
# # plt.show()
#
# mapTech = alt.Chart(schoolData).mark_circle(size=4).encode(
#     latitude='Lat',
#     longitude='Lon',
#     color=alt.Color('Tech',legend=alt.Legend(title="Technology",orient='top-right'),
#                 scale=alt.Scale(scheme='category10'))
# ).properties(
#     height=600,
#     width=800,
#     title='Map of Schools and Technology Selection'
# )
# mapTech.configure_title(
#     fontSize=20,
#     font='Averta',
#     color='gray'
# )
# mapTech.serve()
