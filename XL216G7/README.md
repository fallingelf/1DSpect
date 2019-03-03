Explanation
---
These scripts are used for spectra obtained using 216 cm telescope with instrument of G7 grism.

Instrument
---
1).
Install conda and set up an envirenment for example myenv containing pyiraf;
2).
Revise two variables, Path_Folder_script and Path_Folder_Data, in each Python script;
;----------------------------------------------
G7_packit.py; Lines 90-91
G7_showit.py; Lines 6-7
G7_treat.py;  Lines 168-169
;----------------------------------------------
3).
 a file in
3).
Put yor data folder in the Spectrum folder specified by variable Path_Folder_script;
4).
Revise the Log file and add the nessessery flags such as a, d, o, and c for arc, dome flat, object and companion frames respectively at the end of the corresponding line. And copy the context to new file with the same name to jump the reading problem. 
5).
activate the envirenment and run g7
