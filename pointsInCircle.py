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

#Given center and radius of a circle, gives all integer points which lie inside
#or on the circle radius

def pointsInCircle(xCenter, yCenter, radius):
    x_ = np.arange(xCenter - radius, xCenter + radius + 1, dtype=int)
    y_ = np.arange(yCenter - radius, yCenter + radius + 1, dtype=int)
    x, y = np.where((x_[:,np.newaxis] - xCenter)**2 + (y_ - yCenter)**2 <= radius**2)

    return x_[x], y_[y];
