Explanation
-----------
These scripts are used for spectra obtained using 216 cm telescope with instrument of G7 grism.

Instrument
----------
1).Install conda and set up an envirenment for example mypyraf containing pyiraf, iraf-all;

2).Revise two variables, 'Path_Folder_script' and 'Path_Folder_Data', in each Python script;

;--------------------------------------------------------------------------------------------------

G7_packit.py    #Lines 90-91

G7_showit.py    #Lines 6-7

G7_treat.py     #Lines 168-169

#--------------------------------------------------------------------------------------------------

3).create a new executable file named 'g7' in direction /usr/local/bin containing the following context:

#--------------------------------------------------------------------------------------------------

#!/bin/bash

cd absolute-path-of-data-folder-of-iraf

python3 absolute-path-of-pyscript/G7_treat.py

python3 absolute-path-of-pyscript/G7_packit.py

python3 absolute-path-of-pyscript/G7_showit.py

#---------------------------------------------------------------------------------------------------

4).Put yor data folder in the spectrum folder specified by variable Path_Folder_script;

5).Revise the Log file and add the nessessery flags such as a, d, o, and c for arc, dome flat, object and companion frames 
respectively at the end of the corresponding line. And copy the context to new file with the same name to jump the 
reading problem;

6).activate the envirenment, run g7 and then wait...

>source activate mypyraf

>g7

7).out from the envirment.

>source deactivate mypyraf

Example
-------
a).The revised version of context of the Log file.


||Files          |Obj          |BTime        |Exp.(s)    |R.A.          |Dec.          |Epoch      |Notes||

|20190227001-5  |bias         |17:47:16     |0                                                                   |                                                 

|20190227011-15 |flat         |17:47:40     |150                                               |G7+S2.3+385LP |d|

|20190227017    |fear         |17:47:44     |300                                               |G7+S2.3+385LP |a|

|20190227040    |KZHya        |24:39:47     |900        |10:50:54.00   |25:21:15.0   |2000       |G7+S2.3+385LP |o|

|20190227044    |HD86986      |26:24:41     |60         |10:02:29.00   |+14:33:25.0   |2000       |G7+S2.3+385LP |c|

|20190227058-62 |BIAS         |30:01:02     |0                                                                       |     


| | Files | Obj | BTime | Exp.(s)  | R.A.  | Dec. | Epoch  | Notes |
| --------|:---: |:--: | :----: | :----: | :---: | :-------: | :------: | :------: |
| 20190227001-5| bias  |   17:47:16     | 0.9.8  | 0.9.6   | 0.9.7 |   0.9.8   | 0.9.7 | 0.9.7 |
| [readline](http://thrysoee.dk/editline/)/[editline](http://thrysoee.dk/editline/)       | + (r)  |    + (r)   |  + (r) | + (r)   | + (r) |   + (r)   | + (r) |   +   |
| [\[n\]curses](https://www.gnu.org/software/ncurses/)                                    | + (n)  |    + (n)   |  + (n) | + (n)   |   +   |   + (n)   | + (n) | + (n) |
| [zlib](https://zlib.net/)                                                               |   +    |    +       |   +    | +       |   +   |    +      |   +   |   +   |
| [GSL](https://www.gnu.org/software/gsl/)                                                |   +    |    +       |   +    | +       |   +   |    +      |   +   |   +   |
| [plplot](https://plplot.sourceforge.net)                                                |   +    |    +       |   +    | +       |   +   |    +      |   +   |   +   |
| [OpenMP](http://www.openmp.org/)                                                        |   +    |    +       |   +    | +       |   +   |    +      |   -   |   +   |
| [Magick++](https://imagemagick.org/) / [GraphicsMagick](http://graphicsmagick.org/)     | + (G)  |  + (G)     | + (G)  | + (G/I) |   -   |  + (G)    | + (G) | + (G) |
| [wxWidgets](https://www.wxwidgets.org/)                                                 |   +    |    +       |   +    | +       |   +   |    +      |   -   |   -   |
| [netCDF](https://www.unidata.ucar.edu/software/netcdf/)                                 |   +    |    +       |   +    | +       |   +   |    +      |   +   |   +   |
| [HDF4](https://support.hdfgroup.org/products/hdf4/)                                     |   +    |    +       |   +    | +       |   -   |    -      |   -   |   +   |
| [HDF5](https://support.hdfgroup.org/HDF5/)                                              |   +    |    +       |   +    | +       |   -   |    +      |   +   |   +   |
| [FFTW](http://www.fftw.org/)                                                            |   +    |    +       |   +    | +       |   +   |    +      |   +   |   +   |
| [PROJ.4](http://proj4.org/)                                                             |   -    |    -       |   -    | +       |   -   |    +      |   -   |   +   |
| [GSHHG](http://www.soest.hawaii.edu/wessel/gshhg/)                                      |   -    |    -       |   -    | +       |   -   |    -      |   -   |   +   |
| [MPICH](https://www.mpich.org/)                                                         |   -    |    -       |   -    | -       |   -   |    +      |   -   |   +   |
| [Python](https://www.python.org/)/[NumPy](http://www.numpy.org/)                        |   +    |    +       |   +    | +       |   +   |    +      |   -   |   +   |
| [udunits](https://www.unidata.ucar.edu/software/udunits/)                               |   +    |    +       |   +    | +       |   +   |    +      |   +   |   +   |
| [Eigen](https://eigen.tuxfamily.org/)                                                   |   +    |    +       |   +    | +       |   +   |    +      |   +   |   +   |
| [pslib](http://pslib.sourceforge.net/)                                                  |   +    |    +       |   +    | +       |   +   |    +      |   -   |   +   |
| [ecCodes](https://software.ecmwf.int/wiki/display/ECC/ecCodes+Home)/[GRIB](https://software.ecmwf.int/wiki/display/GRIB)                                    |   +    |    +       |   +    | +       |   +   |    +      |   -   |   +   |
| [GLPK](https://www.gnu.org/software/glpk/)                                              |   -    |    -       |   -    | -       |   -   |    +      |   -   |   -   |
| [Python](https://www.python.org/) module                                                | + (python2-gdl) | + ([python-gdl](https://packages.debian.org/python-gdl)) | + ([python-gdl](https://packages.ubuntu.com/python-gdl)) | +       |   -   |    -      |   -   |   -   |





b).Run steps in the terminal.

>source activate mypyraf

>g7

waiting...

>source deactivate mypyraf
