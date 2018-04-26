# MPhys_Project

MAESTRO (Modelling vAriable Emission in STellar RegiOns): A simulator for variability of sources in star forming regions.

## Getting Started

### Prerequisites

The simulator uses Python 3 and makes use of astropy.


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

* Time intervals at which sky images should be modelled. These can be submitted in a table as for source masses.
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
