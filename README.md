# MPhys_Project

MAESTRO (Modelling vAriable Emission in STellar RegiOns): A simulator for variability of sources in star forming regions.

## Getting Started

### Prerequisites

The simulator uses Python 3 and makes use of: astropy, pillow and matplotlib.


## Using MAESTRO

### User Inputs

The simulator takes inputs of:
* Sources with mass given in terms of solar masses. These can be individually added or submitted in a table with each mass on a new line as the example below shows (lines can be omitted using #)

```
1
2
3
4

```

* You can also use the IMF to distribute masses over a given range for a given number of masses. The ranges and percentage of stars in each range is shown below:

```
Range of masses in solar masses     percentage
0.01 - 0.08                             37
0.08 - 0.5                              48
0.5 - 1                                 8.9
1 - 8                                   5.7
8 - 120                                 0.4
```

If not all mass ranges are used the percentages are re-assigned to not include groups that aren't used. If a min/max mass is used within a range then the whole range is used but stars below/above the min/max mass are deleted. This reduces the total number of stars and a warning is shown.

* Time intervals at which sky images should be modeled. These can be submitted in a table as for source masses.
* Cluster size (parsecs)
* Distance to cluster (parsecs)
* Field of view (arcminutes) -  used to produce a sky image.
* Selection of source distribution function. Current choices include a random or uniform distribution.

### Output

MAESTRO will create a table of information for the sources provided as shown below:

```
Source Mass    Type    Binary    X coordinate    Y coordinate


```


On running a model sky image will be created and displayed on the left which can be viewed at the times as input. A light curve for each source can be viewed on the right.

## Ideas for the future

Additions to this project that may be of use in the future.

## Authors

* **Ellen Leahy** - *University of Manchester 4th Year Student - Physics with Astrophysics* - *(Project manager)*
* **Joe Stickley** - *University of Manchester 4th Year Student - Physics*

See also the list of [contributors](https://github.com/ellenleahy-95/mphys_project/contributors) who participated in this project.

## Acknowledgments

* Gary Fuller
* Adam Avison
