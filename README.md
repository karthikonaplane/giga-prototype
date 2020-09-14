# Installation

Make sure all dependencies are installed using the following links:

python3>=3.5.5
MacOS: (https://docs.python-guide.org/starting/install3/osx/)
You will need to install GCC and Homebrew to make this work, directions are in the above link

pip==20.1.1
Should be installed automatically by Homebrew when installing Python3

pandas==0.25.1
(https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html)

matplotlib==3.1.1
(https://pypi.org/project/vega-datasets/)

rasterio==1.1.3
(https://rasterio.readthedocs.io/en/latest/installation.html)

numpy==1.17.2
(https://scipy.org/install.html)

grispy==0.0.2 
(https://pypi.org/project/grispy/) 

wheel==0.34.2
(https://pypi.org/project/wheel/)

altair==4.0.1
(https://altair-viz.github.io/getting_started/installation.html)

geopandas==0.7.0	
(https://geopandas.org/install.html)

vega_datasets==0.8.0
Should be installed with altair
Otherwise: (https://pypi.org/project/vega-datasets/)


# Configuration
Next, check the technology and project input files to make sure that the default inputs match with the context in which you are planning your own project. 
These two files are:

`projectInputs.py` - defines demographic and usage inputs
`techInputs.py` - defines connectivity, power requirements, energy generation, and energy storage costs, performance, and labor times

Then, verify that the labor rates at the bottom of `projectInputs.py` and the annual ISP fees in `techInputs.py` are correct. 
These are the most likely to vary from region to region. Other costs such as hardware costs are less likely to vary between regions (though tarriffs might
cause significant discrepancies), and the connectivity needs of teachers, students, and the community are likely to vary more between schools within a 
region than between regional averages.

Select the configuration options in `projectInputs.py` under configuration. Both P0 and P1 computations are on by default.

Adjust the country input files, under the `args.Country` section.

`schoolDataPath` should be the path to an xlsx file with columns described in model documentation
`popDataPath` should be a 100 meter square population GeoTiff file

Note that you can define the “country” to be anything, so if a country has provided multiple school datasets you can define 
each one with a unique ID. The script was initially written to take these parameters from the command line, however defining 
the input files directly in the script is an easy way to save multiple configurations and inputs, and avoids errors of mixing and matching the wrong inputs.

The technology selection flow is contained in `analysis.py`. Adjust the fiber radii, WISP radii, and flowdown order if the 
default fiber->WISP->cell->satellite order is different in your locale.


# Running
Running the script is simple:

>python3 analysis.py -C ‘countryname’

Where `countryname` is the value you have selected for your `args.Country`. The analysis will output to `school_output.csv` which you can then analyze using
`plotAnalysis.py`.

`plotAnalysis.py` has a similar `args.Country` section where you can hardcode the path to your `school_output.csv` and a corresponding shapefile for 
the country borders. You can run this with:

>python3 plotAnalysis.py -C ‘countryname’
