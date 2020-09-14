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

import numpy as np
import pandas as pd



def computeCosts(schoolData,pjIn,techIn,techTypes,verbose):

    #Setup DataFrame
    costCols = (['speed','power','battery_overnight','battery_annual',
                'solar_overnight','solar_annual',
                 'overnight_hardware_fixed','overnight_labor_fixed',
                 'overnight_hardware_variable','overnight_labor_variable_time',
                 'setup_fees','annual_hardware','annual_labor_time','annual_fees',
                 'overnight_fixed','overnight_variable','annual_cost'])


    techCosts = pd.DataFrame(index=techTypes,columns=costCols)

    schoolData['Overnight Cost'] = ''
    schoolData['Annual Cost'] = ''
    schoolData['Overnight Power Cost'] = ''
    schoolData['Annual Power Cost'] = ''


    #======Compute fixed, variable, and operating costs for each type of technlogy

    #Load data into dataframe
    for dicts in techTypes:
        for key, value in getattr(techIn,dicts).items():
            techCosts[key][dicts] = value

    techCosts = techCosts.fillna(0)
    if verbose:
        print(techCosts)

    #Compute fixed and variable costs

    # techCosts['battery_overnight'] = ((techCosts['power']/1000 * (24-techIn.solar['daylight']) * techIn.battery['costperkWh'])
    #                                  + techIn.battery['overnight_hardware_fixed']
    #                                  + techIn.battery['overnight_labor_fixed'] * pjIn.demo['labor_cost_skilled'])

    techCosts['battery_overnight'] = ((techCosts['power']/1000 * (24-techIn.solar['daylight'])) *
                                        (techIn.battery['overnight_hw']
                                        + techIn.battery['overnight_labor_regular'] * pjIn.demo['labor_cost_regular']
                                        + techIn.battery['overnight_labor_skilled'] * pjIn.demo['labor_cost_skilled']))

    # techCosts['solar_overnight'] = (techCosts['power']/1000 * techIn.solar['costperkW']
    #                                  + techIn.solar['overnight_hardware_fixed']
    #                                  + techIn.solar['overnight_labor_fixed'] * pjIn.demo['labor_cost_skilled'])

    techCosts['solar_overnight'] = (techCosts['power']/1000 *
                                      (techIn.solar['overnight_hw']
                                     + techIn.solar['overnight_labor_regular'] * pjIn.demo['labor_cost_regular']
                                     + techIn.solar['overnight_labor_skilled'] * pjIn.demo['labor_cost_skilled']))

    # techCosts['battery_annual'] = (techCosts['battery_overnight'] * techIn.battery['annual_hardware']
    #                                  + techIn.battery['annual_labor_time'] * pjIn.demo['labor_cost_skilled'])

    techCosts['battery_annual'] = ((techCosts['power']/1000 * (24-techIn.solar['daylight'])) *
                                    (techIn.battery['annual_hardware'] +
                                   + techIn.battery['annual_labor_regular'] * pjIn.demo['labor_cost_regular']
                                   + techIn.battery['annual_labor_skilled'] * pjIn.demo['labor_cost_skilled']))

    # techCosts['solar_annual'] = (techCosts['solar_overnight'] * techIn.solar['annual_hardware']
    #                              + techIn.solar['annual_labor_time'] * pjIn.demo['labor_cost_skilled'])

    techCosts['solar_annual'] = (techCosts['power']/1000 *
                                 (techIn.solar['annual_hardware'] +
                                + techIn.solar['annual_labor_regular'] * pjIn.demo['labor_cost_regular']
                                + techIn.solar['annual_labor_skilled'] * pjIn.demo['labor_cost_skilled']))


    techCosts['overnight_fixed'] = (techCosts['setup_fees'] +
                                    techCosts['overnight_hardware_fixed'] +
                                    techCosts['overnight_labor_fixed'] * pjIn.demo['labor_cost_skilled']
                                    )

    techCosts['overnight_variable'] = (techCosts['overnight_hardware_variable'] +
                                       techCosts['overnight_labor_variable_time'] * pjIn.demo['labor_cost_regular'])

    techCosts['annual_cost'] = (techCosts['annual_hardware'] * techCosts['overnight_fixed'] +
                                techCosts['annual_labor_time'] * pjIn.demo['labor_cost_regular'] +
                                techCosts['annual_fees'])

    if verbose:
        print(techCosts['annual_cost'])

    #======Compute costs for each school

    for schoolIndex in schoolData.index:
        if schoolData['Tech'][schoolIndex] == 'fiber':
            schoolData['Overnight Cost'][schoolIndex] = (
                        techCosts['overnight_fixed'][schoolData['Tech'][schoolIndex]] +
                        techCosts['overnight_variable'][schoolData['Tech'][schoolIndex]] * schoolData['Distance to Nearest Fiber'][schoolIndex])
        if (schoolData['Tech'][schoolIndex] != 'fiber') & (schoolData['Tech'][schoolIndex] != ''):
            schoolData['Overnight Cost'][schoolIndex] = (
                techCosts['overnight_fixed'][schoolData['Tech'][schoolIndex]])

        if (schoolData['Tech'][schoolIndex] != ''):
            schoolData['Annual Cost'][schoolIndex] = techCosts['annual_cost'][schoolData['Tech'][schoolIndex]]

        #If there's grid data and the school has no power, or there's no grid data, assume the school needs battery and solar

        if 'elec_grid' in schoolData.columns:
            if(schoolData['elec_grid'][schoolIndex] == 'No'):
                schoolData['Overnight Power Cost'][schoolIndex] = techCosts['battery_overnight'][schoolData['Tech'][schoolIndex]] + techCosts['solar_overnight'][schoolData['Tech'][schoolIndex]]
                schoolData['Annual Power Cost'][schoolIndex] = techCosts['battery_annual'][schoolData['Tech'][schoolIndex]] + techCosts['solar_annual'][schoolData['Tech'][schoolIndex]]

            #If the school has grid power, size battery based on if it has a generator (which would take the place of a battery)
            if (schoolData['elec_grid'][schoolIndex] == 'Yes'):
                if((schoolData['generator'][schoolIndex] == 'No')):
                    schoolData['Overnight Power Cost'][schoolIndex] = techCosts['battery_overnight'][schoolData['Tech'][schoolIndex]]
                    schoolData['Annual Power Cost'][schoolIndex] = techCosts['battery_annual'][schoolData['Tech'][schoolIndex]]

                if((schoolData['generator'][schoolIndex] == 'Yes')):
                    schoolData['Overnight Power Cost'][schoolIndex] = 0.0
                    schoolData['Annual Power Cost'][schoolIndex] = 0.0

        else:
            schoolData['Overnight Power Cost'][schoolIndex] = techCosts['battery_overnight'][schoolData['Tech'][schoolIndex]] + techCosts['solar_overnight'][schoolData['Tech'][schoolIndex]]
            schoolData['Annual Power Cost'][schoolIndex] = techCosts['battery_annual'][schoolData['Tech'][schoolIndex]] + techCosts['solar_annual'][schoolData['Tech'][schoolIndex]]



    return schoolData['Overnight Cost'], schoolData['Annual Cost'], schoolData['Overnight Power Cost'], schoolData['Annual Power Cost']

    #return costsPD
