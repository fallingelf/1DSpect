from pyraf import iraf
import os

Path_Folder_script='/home/host-name/IRAF/rfscript/'
Path_Folder_Data='/home/host-name/IRAF/spectrum/'

i=0;Path_Folder_Obj=Path_Folder_Data+os.listdir(Path_Folder_Data)[i]

result_path=Path_Folder_Obj+'/'+os.listdir(Path_Folder_Data)[i]+'_result';
os.chdir(result_path+'/fits/');os.system('cd '+result_path+'/fits/')

iraf.noao.twodspec()
iraf.noao.twodspec.longslit()
iraf.noao.twodspec.longslit.splot('*');
