from pyraf import iraf
import os,shutil
import numpy as np

def expand_name(Files):
    if '-' in Files:
        part_Files=Files.replace('-',' ').split()
        N=1-int(part_Files[0][-3:])+int(part_Files[1])
        name_expand=[]
        for i in range(N):
            name_expand.append([])
            name_expand[-1]=part_Files[0][:-3]+'-'+str(int(part_Files[0][-3:])+i).zfill(4)+'.fit'
    else:
        name_expand=Files[:-3]+'-'+str(Files[-3:]).zfill(4)+'.fit';
        N=1
    return N,name_expand

def expand_inf_file(inf_file):
    N=expand_name(inf_file[-1][0])[0]
    name_expand=expand_name(inf_file[-1][0])[1]
    list_inf_tail=inf_file[-1][1:]
    if N > 1:
      for i in range(N):   
        inf_file[-1]=[name_expand[i]]+list_inf_tail
        if i<N-1:
            inf_file.append([])
    else:
        inf_file[-1]=[name_expand]+list_inf_tail
    return inf_file

def find_files(PATH,key_name,flag=-1):                        #from folder(PATH) filter filenames contaning key_name  
    files_all=os.listdir(PATH);file_object=[]
    if flag==0:
        for j in range(len(files_all)):
            if key_name == files_all[j][:len(key_name)]:
                file_object.append(files_all[j])
    if flag==-1:
        for j in range(len(files_all)):
            if key_name == files_all[j][flag*len(key_name):]:
                file_object.append(files_all[j])
    return sorted(file_object)

def reflesh(list_str,str_unvalu,flag):
    j=0
    while j < len(list_str):
        if list_str[j][flag] == str_unvalu:
            iraf.imdel(list_str[j][0],veri=0)             #delete the term of list
            del list_str[j]                        #delete associated image
        else:
            j+=1
    return list_str

def distance_points(x1,y1,x2,y2):
    x1=x1.replace(':',' ').split();x1=float(x1[0])+float(x1[1])/60+float(x1[2])/3600
    y1=y1.replace(':',' ').split();y1=float(y1[0])+float(y1[1])/60+float(y1[2])/3600
    x2=x2.replace(':',' ').split();x2=float(x2[0])+float(x2[1])/60+float(x2[2])/3600
    y2=y2.replace(':',' ').split();y2=float(y2[0])+float(y2[1])/60+float(y2[2])/3600
    return (x1-x2)**2+(y1-y2)**2

def find_stand_path(stand_name,PATH):
    stand_star_txt=open(PATH+'stand_stars','r')
    stand_star_list=stand_star_txt.readlines()
    stand_star_txt.close()
    for j in range(len(stand_star_list)):
        if stand_name.lower() in stand_star_list[j]:
            return '/iraf/iraf/noao/lib/onedstds/'+stand_star_list[j].split()[0]

def mkdir(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

def write_files2file(file_name,key_words,rw='w'):
    key_words=key_words.split(',')
    txt_file_pn=open(file_name,rw)
    for i in range(len(key_words)):
        txt_file_pn.write('\n'.join(find_files(os.getcwd(),key_words[i])))
        if i !=len(key_words):
            txt_file_pn.write('\n')
    txt_file_pn.close()
    return 

def write_list2file(file_name,list_name):
    with open(file_name,'w') as f:
        f.write('\n'.join(list_name))
        f.close()
 

Path_Folder_script='/home/wqs/IRAF/rfscript/'
Path_Folder_Data='/home/wqs/IRAF/spectrum/'

i=0;Path_Folder_Obj=Path_Folder_Data+os.listdir(Path_Folder_Data)[i]
os.chdir(Path_Folder_Obj);os.system('cd '+Path_Folder_Obj)

iraf.noao.imred()
iraf.noao.imred.kpnoslit();iraf.noao.onedspec()

result_path=Path_Folder_Obj+'/'+os.listdir(Path_Folder_Data)[i]+'_result';mkdir(result_path)
need_files=find_files(Path_Folder_Obj,'_ca.fits')+find_files(Path_Folder_Obj,'_co.fits')
[shutil.copy(Path_Folder_Obj+'/'+need_files[j],result_path) for j in range(len(need_files))]

iraf.noao.imred()
iraf.noao.imred.kpnoslit();iraf.noao.onedspec()
os.chdir(result_path);os.system('cd '+result_path)
[iraf.noao.imred.kpnoslit.scopy(result_path+'/'+need_files[j],result_path+'/'+need_files[j],format='onedspec',rebin=0) for j in range(len(need_files))]
[iraf.noao.onedspec.wspectext(need_files[j]+'.0001.fits',need_files[j].replace('fits','dat'),header=0,wformat="%0.2f") for j in range(len(need_files))]
[iraf.noao.onedspec.wspectext(need_files[j]+'.0001.fits',need_files[j].replace('fits','txt'),header=1,wformat="%0.2f") for j in range(len(need_files))]

garbage_files=find_files(result_path,'001.fits')
[os.remove(result_path+'/'+garbage_files[j]) for j in range(len(garbage_files))]
mkdir(result_path+'/dat/');mkdir(result_path+'/fits/');mkdir(result_path+'/txt/');
fits_files=find_files(result_path,'.fits');dat_files=find_files(result_path,'.dat');txt_files=find_files(result_path,'.txt')
[shutil.move(result_path+'/'+fits_files[j],result_path+'/fits/') for j in range(len(fits_files))]
[shutil.move(result_path+'/'+dat_files[j],result_path+'/dat/') for j in range(len(dat_files))]
[shutil.move(result_path+'/'+txt_files[j],result_path+'/txt/') for j in range(len(txt_files))]


