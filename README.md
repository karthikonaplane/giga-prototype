# About

The COVID-19 pandemic has created the largest disruption of education systems in history, affecting nearly 1.6 billion learners in more than 190 countries; school and learning space closures have impacted 94 per cent of the world’s student population. And, even before the pandemic, there were 3.6 billion people in the world without access to the Internet. This disruption in learning - especially those with pre-existing disparities in education and access - threatens to erase decades of progress, as closures of educational institutions hamper the provision of essential services to the entire community. The promise of future learning and living needs innovation and the internet to deliver quality education and services. 

How much will it cost to connect a school to the internet? How much bandwidth does a school need and what technology is best suited to deliver it? What will it cost to keep that school connected? And how will connectivity impact the community around that school?

The models contained here are used to quickly answer the above questions. Briefly they:

1. De-duplicate schools and consolidate multiple schools on the same site
2. Compute the school and local census if enrollment data doesn't exist
3. Determine the bandwidth needed
4. Selects a technology
5. Computes power requirements, and if grid power is unavailable or unreliable, sizes a solar and battery solution
6. Compute "overnight" cost to connect the school (labor and hardware). "Overnight" means that the work happens instantly, and doesn't account for the cost of capital or financing during the construction period. Also referred to as the Capital Expense (CapEx).
7. Computes annual costs to keep the school connected and all hardware maintained. Also referred to as the Operational Expense (OpEx).

Several assumptions have been made in building each model, especially around user needs and specific usage patterns. In addition, costing estimates are preliminary; models and inputs be refined with feedback from users and stakeholders.

# Installation

Make sure all dependencies are installed using the following links:

python3>=3.5.5
MacOS: https://docs.python-guide.org/starting/install3/osx/
You will need to install GCC and Homebrew to make this work, directions are in the above link

pip==20.1.1
Should be installed automatically by Homebrew when installing Python3

pandas==0.25.1
https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html

matplotlib==3.1.1
https://pypi.org/project/vega-datasets/

rasterio==1.1.3
https://rasterio.readthedocs.io/en/latest/installation.html

numpy==1.17.2
https://scipy.org/install.html

grispy==0.0.2 
https://pypi.org/project/grispy/

wheel==0.34.2
https://pypi.org/project/wheel/

altair==4.0.1
https://altair-viz.github.io/getting_started/installation.html

geopandas==0.7.0
https://geopandas.org/install.html)

vega_datasets==0.8.0
Should be automatically installed with altair
Otherwise: https://pypi.org/project/vega-datasets/


# Configuration
Next, check the technology and project input files to make sure that the default inputs match with the context in which you are planning your own project.  These two files are:

`projectInputs.py` - defines demographic and usage inputs
`techInputs.py` - defines connectivity, power requirements, energy generation, and energy storage costs, performance, and labor times

Then, verify that the labor rates at the bottom of `projectInputs.py` and the annual ISP fees in `techInputs.py` are correct. These are the most likely to vary from region to region. Other costs such as hardware costs are less likely to vary between regions (though tarriffs might cause significant discrepancies), and the connectivity needs of teachers, students, and the community are likely to vary more between schools within a region than between regional averages.

Select the configuration options in `projectInputs.py` under configuration. Both P0 and P1 computations are on by default.

Adjust the country input files, under the `args.Country` section.

`schoolDataPath` should be the path to an xlsx file with columns described in model documentation
`popDataPath` should be a 100 meter square population GeoTiff file

Note that you can define the “country” to be anything, so if a country has provided multiple school datasets you can define each one with a unique ID. The script was initially written to take these parameters from the command line, however defining the input files directly in the script is an easy way to save multiple configurations and inputs, and avoids errors of mixing and matching the wrong inputs.

The technology selection flow is contained in `analysis.py`. Adjust the fiber radii, WISP radii, and flowdown order if the default fiber->WISP->cell->satellite order is different in your locale.


# Running
Running the script is simple:

>python3 analysis.py -C ‘countryname’

Where `countryname` is the value you have selected for your `args.Country`. The analysis will output to `school_output.csv` which you can then analyze using `plotAnalysis.py`.

`plotAnalysis.py` has a similar `args.Country` section where you can hardcode the path to your `school_output.csv` and a corresponding shapefile for the country borders. You can run this with:

>python3 plotAnalysis.py -C ‘countryname’

# About UNICEF:
UNICEF promotes the rights and wellbeing of every child, in everything we do. Together with our partners, we work in 190 countries and territories to translate that commitment into practical action, focusing special effort on reaching the most vulnerable and excluded children, to the benefit of all children, everywhere.

For more information about UNICEF and its work for children, visit www.unicef.org.

Follow UNICEF on [Twitter](https://twitter.com/unicefmedia) and [Facebook](https://www.facebook.com/unicef/)

# About ACTUAL:
ACTUAL gives infrastructure originators, investors, and other stakeholders confidence as they model and track the cost, impact, and outcomes of sustainable and net-zero infrastructure projects. Visit www.actualhq.com or [contact us](mailto:hello@actualhq.com) to learn more about how our digital-twin based models can help unlock new savings and revenue streams for your projects.

Follow ACTUAL on [Twitter](https://twitter.com/ActualHQ) and visit our [blog](http://blog.actualhq.com) to learn more about our other projects and perspectives.

# About Giga: 

Some 3.6 billion people in the world do not have access to the Internet. The lack of access to the internet means exclusion, marked by the lack of access to the wealth of information available online, fewer resources to learn and grow, and limited opportunities for the most vulnerable children and youth to fulfill their potential. Closing the digital divide requires global cooperation, leadership, and innovation in finance and technology. 

Giga is a UNICEF-ITU global initiative to connect every school to the Internet and every young person to information, opportunity and choice. Connect with us by visiting https://gigaconnect.org and following us on [Twitter](https://twitter.com/Gigaconnect). 

