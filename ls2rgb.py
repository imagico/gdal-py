#!/usr/bin/env python
#--------------------------------------------------------------------------
# ls2rgb.py
# 
# assembles three landsat channels to a rgb geotiff with gdal
#
# ls2rgb.py is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ls2rgb.py is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with dem_water.  If not, see <http://www.gnu.org/licenses/>.
#
#--------------------------------------------------------------------------

try:
    from osgeo import gdal
    from osgeo.gdalconst import *
    gdal.TermProgress = gdal.TermProgress_nocb
except ImportError:
    import gdal
    from gdalconst import *
    
try:
    import numpy
except ImportError:
    import Numeric as numpy
    
try:
    from osgeo import gdalnumeric
except ImportError:
    import gdalnumeric

from math import *
import sys

def Usage():
    print 'ls2rgb.py - assembles three landsat channels to a rgb geotiff with gdal'
    print
    print 'Copyright (C) 2013 Christoph Hormann'
    print 'This program comes with ABSOLUTELY NO WARRANTY;'
    print 'This is free software, and you are welcome to redistribute'
    print 'it under certain conditions; see COPYING for details.'
    print
    print 'Usage: ls2rgb.py [-g gamma] [-s scale] red_file green_file blue_file outfile'
    print
    sys.exit(1)

red_file = None
green_file = None
blue_file = None
outfile = None
format = 'GTiff'
type = GDT_Byte
gamma = 2.0
scale = 1.0
        
gdal.AllRegister()
argv = gdal.GeneralCmdLineProcessor( sys.argv )
if argv is None:
    sys.exit(0)
    
i = 1
while i < len(sys.argv):
    arg = sys.argv[i]

    if arg == '-g':
        i = i + 1
        gamma = float(sys.argv[i])

    elif arg == '-s':
        i = i + 1
        scale = float(sys.argv[i])
        
    elif red_file is None:
        red_file = arg

    elif green_file is None:
        green_file = arg

    elif blue_file is None:
        blue_file = arg

    elif outfile is None:
        outfile = arg

    else:
        Usage()

    i = i + 1

if red_file is None:
    Usage()
if green_file is None:
    Usage()
if blue_file is None:
    Usage()
if  outfile is None:
    Usage()

red_dataset = gdal.Open( red_file, GA_ReadOnly )
green_dataset = gdal.Open( green_file, GA_ReadOnly )
blue_dataset = gdal.Open( blue_file, GA_ReadOnly )

out_driver = gdal.GetDriverByName(format)

outdataset = out_driver.Create(outfile, red_dataset.RasterXSize, red_dataset.RasterYSize, 3, type)
outdataset.SetGeoTransform( red_dataset.GetGeoTransform() )
outdataset.SetProjection( red_dataset.GetProjection() )

numtype = gdalnumeric.GDALTypeCodeToNumericTypeCode(type)

red_band = red_dataset.GetRasterBand(1)
if (green_dataset.RasterCount > 1):
    green_band = green_dataset.GetRasterBand(2)
else:
    green_band = green_dataset.GetRasterBand(1)
if (blue_dataset.RasterCount > 2):
    blue_band = blue_dataset.GetRasterBand(3)
else:
    blue_band = blue_dataset.GetRasterBand(1)

red_outband = outdataset.GetRasterBand(1)
green_outband = outdataset.GetRasterBand(2)
blue_outband = outdataset.GetRasterBand(3)

gdal.TermProgress(0.0)

for i in range(red_band.YSize - 1, -1, -1):
    red_scanline = red_band.ReadAsArray(0, i, red_band.XSize, 1, red_band.XSize, 1).astype(float)
    green_scanline = green_band.ReadAsArray(0, i, green_band.XSize, 1, green_band.XSize, 1).astype(float)
    blue_scanline = blue_band.ReadAsArray(0, i, blue_band.XSize, 1, blue_band.XSize, 1).astype(float)
        
    red_scanline = numpy.power(red_scanline*scale/65535.0, 1.0/gamma)*255.0
    green_scanline = numpy.power(green_scanline*scale/65535.0, 1.0/gamma)*255.0
    blue_scanline = numpy.power(blue_scanline*scale/65535.0, 1.0/gamma)*255.0

    red_outband.WriteArray(red_scanline.astype(numtype), 0, i)
    green_outband.WriteArray(green_scanline.astype(numtype), 0, i)
    blue_outband.WriteArray(blue_scanline.astype(numtype), 0, i)
    
    gdal.TermProgress((float)(red_band.YSize-i)/red_band.YSize)

