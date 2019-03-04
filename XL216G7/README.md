Explanation
---
These scripts are used for spectra obtained using 216 cm telescope with instrument of G7 grism.

Instrument
---
1).Install conda and set up an envirenment for example mypyraf containing pyiraf, iraf-all;

2).Revise two variables, ¡®Path_Folder_script¡¯ and ¡®Path_Folder_Data¡¯, in each Python script;
;----------------------------------------------
G7_packit.py    #Lines 90-91
G7_showit.py    #Lines 6-7
G7_treat.py     #Lines 168-169
;----------------------------------------------

3).create a new executable file named ¡®g7¡¯ in direction /usr/bin/local/ containing the following context:
;----------------------------------------------------
#bash shell
python3 absolute-path-of-pyscript/G7_treat.py
python3 absolute-path-of-pyscript/G7_packit.py
python3 absolute-path-of-pyscript/G7_showit.py
;-----------------------------------------------------

4).Put yor data folder in the spectrum folder specified by variable Path_Folder_script;

5).Revise the Log file and add the nessessery flags such as a, d, o, and c for arc, dome flat, object and companion frames 
respectively at the end of the corresponding line. And copy the context to new file with the same name to jump the 
reading problem;

6).activate the envirenment, run g7 and then wait...
>source activate mypyraf
>g7

7).out from the envirment.
>source deactivate mypyraf