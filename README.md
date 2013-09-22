
GDAL based python scripts for geodata processing
================================================

This repository is for [GDAL](http://www.gdal.org/) based python tools for geodata processing

ls2rgb.py
---------

This script assembles three landsat channels into an rgb geotiff file including value scaling and gamma correction.

Usage:

`ls2rgb.py [-g gamma] [-s scale] red_file green_file blue_file outfile`

Options:

* `-g`: Gamma correction.  Default: 2.0
* `-s`: value scaling.  Default: 1.0
* `red_file` `green_file` `blue_file`: Input image files.  If these are not single channel the first, second and third channel are used.  This allows processing already assembled rgb images.
* `outfile`: file name for output

Legal stuff
-----------

This program is licensed under the GNU GPL version 3.

Copyright 2013 Christoph Hormann

