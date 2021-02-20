# astropi2021
## Table of contents
* [Technicalities](#technicalities)
* [Purpose of this project](#purpose-of-this-project)
* [Algorithm and meaning](#algorithm-and-meaning)

## Technicalities
The code is intended for the RaspberryPi 3B+, and was tested on Python 3.5 but should also work on older versions of Python3 :snake:
The images are like this:
./sample_earth.png
## Purpose of this project
We intend to calculate the albedo values of the photographed surfaces of Earth from the ISS. By gathering this information, we are able to discover the theoretical temperature in that
area and make assumptions about greenhouse effect and aerosols, thus reaching a conclusion on the climate state of our planet. :earth_africa:
## Algorithm and meaning
During daytime on the ISS, the pi will take photos. During night time, it will make computations.
For a given photo, the program will compute first the light directions, then the normal and albedo maps. The albedo will be calculated both from the original image and the albedo map
of the image, by the blank-paper-sheet-of-albedo-0.65 relative rule -> http://albedodreams.info/how_to/how-to-calculate-albedo-yourself/ .

After computing the albedo, using the Stefan-Boltzmann law, we compute the temperature of the photographed surface. This doesn't take into account the greenhouse effect, so the 
temperatures are in fact lower than the ones recorded on Earth. The difference will give us answers regarding the greenhouse effect and climate change.

