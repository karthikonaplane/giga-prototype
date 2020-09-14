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

#General technology inputs framework, using Kenya data as the default.
#Create a new file for each country
#To be extended with more granular regional

import pandas as pd

fiber = {
    'speed' : 1500, #Mbps
    'overnight_hardware_fixed' : 1200, #usd per school
    'overnight_labor_fixed' : 5, #hrs per school
    'overnight_hardware_variable' : 1000, #usd per km
    'overnight_labor_variable_time' : 10, #hrs/km
    'setup_fees' : 250, #usd per school
    'annual_hardware' : 0.2, #percentage of upfront fixed cost into mx
    'annual_labor_time' : 10, #hrs/school connection
    'annual_fees' : 2000, #Annual ISP fees
    'power' : 500 #W
}

cell2G = {
    'speed' : 0.0625, #Mbps
    'overnight_hardware_fixed' : 75, #usd per schhol
    'overnight_labor_fixed' : 5, #hrs, per school
    'setup_fees' : 20, #usd/school
    'annual_hardware' : 0.2, #percentage of upfront hardware cost into mx
    'annual_labor_time' : 2, #hrs/school connection
    'annual_fees' : 1200, #Annual ISP fees
    'power' : 10 #W
}

cell3G = {
    'speed' : 2, #Mbps
    'overnight_hardware_fixed' : 150, #usd per schhol
    'overnight_labor_fixed' : 5, #hrs, per school
    'setup_fees' : 75, #usd/school
    'annual_hardware' : 0.2, #percentage of upfront hardware cost into mx
    'annual_labor_time' : 2, #hrs/school connection
    'annual_fees' : 1200, #Annual ISP fees
    'power' : 10 #W

}

cell4G = {
    'speed' : 40, #Mbps
    'overnight_hardware_fixed' : 300, #usd per schhol
    'overnight_labor_fixed' : 5, #hrs, per school
    'setup_fees' : 75, #usd/school
    'annual_hardware' : 0.2, #percentage of upfront hardware cost into mx
    'annual_labor_time' : 2, #hrs/school connection
    'annual_fees' : 1200, #Annual ISP fees
    'power' : 10 #W

}

WISP = {
    'speed' : 400, #Mbps - https://dl.ubnt.com/datasheets/PowerBeam_ac_ISO/PowerBeam_AC_Gen2_DS.pdf
    'overnight_hardware_fixed' : 1500, #usd per schhol
    'overnight_labor_fixed' : 10, #hrs, per school
    'setup_fees' : 200, #usd/school
    'annual_hardware' : 0.2, #percentage of upfront hardware cost into mx
    'annual_labor_time' :5, #hrs/school connection
    'annual_fees' : 2000, #Annual ISP fees
    'power' : 200 #W

}

satellite = {
    'speed' : 150, #Mbps
    'overnight_hardware_fixed' : 4000, #usd per schhol -- from USAID tool
    'overnight_labor_fixed' : 5, #hrs, per school
    'setup_fees' : 200, #usd/school
    'annual_hardware' : 0.2, #percentage of upfront hardware cost into mx
    'annual_labor_time' :2, #hrs/school connection
    'annual_fees' : 3000, #Annual ISP fees
    'power' : 200 #W

}

battery = {
    'overnight_hw' : 461, #USD/kWh - Tesla Powerwall pricing, in line with developing world estimates from https://phys.org/news/2018-09-world-bank-big-batteries-solar.html
    'overnight_labor_regular' : .75, #hrs/kW regular labor, per school
    'overnight_labor_skilled' : 1.25, #hrs/kW skilled labor, per school
    'annual_hardware' : 27.60, #USD/kWh annual
    'annual_labor_regular' :0.125, #hrs/kWh/school connection
    'annual_labor_skilled' :0.075, #hrs/kWh/school connection
}

solar = {
    'overnight_hw' : 1820, #USD/kW - https://docs.google.com/spreadsheets/d/1isH_4ckd9_DAfuWOkKmU5B8fafWSdTWSFUDKt2aL9Bc/edit#gid=0
    'overnight_labor_regular' : 4, #hrs/kW regular labor, per school
    'overnight_labor_skilled' : 4, #hrs/kW skilled labor, per school
    'annual_hardware' : 165, #USD/kW annual
    'annual_labor_regular' :2, #hrs/kW/school connection
    'annual_labor_skilled' :2, #hrs/kW/school connection
    'daylight' : 12 #hrs/day (equatorial)
}


performance = {
    #These have fixed cost and variable costs that scale with speed - to build in
}
