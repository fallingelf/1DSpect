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
 

def check_log(path_log,obs_date,path_std):
    if os.path.exists('ERROR.dat'):
        os.remove('ERROR.dat')
    with open(path_log,'r') as f:
        txt_log=f.readlines();f.close()
    error_log='';standstars=[];
    for j in range(len(txt_log)):      
        if obs_date == txt_log[j][:8]:   #search for list of information of files; the list contains data.
            txt_log[j]=txt_log[j].split();
            if txt_log[j][-1].lower().replace('/','')=='c':
                standstars.append(txt_log[j][1].lower().replace('/',''))
            if txt_log[j][1].lower().replace('/','')=='bias':          #bias                
                if len(txt_log[j])==4:
                    continue
                else:
                    error_log=error_log+('bias      '+'    Error: length is not Four!'+'    ROW:'+str(j+1)+'\n')
                    continue
            if txt_log[j][1].lower().replace('/','')=='flat':          #flat 
                if len(txt_log[j])==6:                         
                    continue
                else:
                    error_log=error_log+('flat      '+'    Error: length is not Six! '+'    ROW:'+str(j+1)+'\n')
                    continue
            if txt_log[j][1].lower().replace('/','')=='fear':         #fear  
                if len(txt_log[j])==6:                       
                    continue
                else:
                    error_log=error_log+('fear      '+'    Error: length is not Six! '+'    ROW:'+str(j+1)+'\n')   
                    continue
            if txt_log[j][-1].lower().replace('/','')=='i':          #image 
                if len(txt_log[j])==9:                          
                    continue
                else:
                    error_log=error_log+('image     '+'    Error: length is not Nine!'+'    ROW:'+str(j+1)+'\n')
                    continue
            if txt_log[j][-1].lower().replace('/','')=='o':         #object 
                if len(txt_log[j])==9:                           
                    continue
                else:
                    error_log=error_log+('object    '+'    Error: length is not Nine!'+'    ROW:'+str(j+1)+'\n')
                    continue
            if txt_log[j][-1].lower().replace('/','')=='c':         #companion
                if len(txt_log[j])==9:                           
                    continue
                else:
                    error_log=error_log+('companion '+'    Error: length is not Nine!'+'    ROW:'+str(j+1)+'\n')
                    continue
    if len(standstars) != 0:   
        with open(path_std+'stand_stars','r') as f:
            stand_stars_txt=f.read();f.close()
        for j in range(len(standstars)):
            if standstars[j].lower() not in stand_stars_txt:
                error_log=error_log+(standstars[j]+' is Not a normal standard stars'+'\n')
    if len(error_log)!=0:
        with open('ERROR.dat','w') as f:
            f.write(error_log);f.close()
        print('################################################')
        print('ERROR Exist!');
        print('------------------------------------------------')
        print(error_log);
        print('------------------------------------------------')
        print('Please revise your log txt!')
        flag=input('input [Y]/N to continue\n');rewind=''
        while rewind!='NEXT':
            if flag.lower()=='y' or flag.lower()=='':
                check_log(path_log,obs_date,path_std);break
            if flag.lower()=='n':
                print('------------------------------------------------')
                print('ERROR Exist!');print(error_log);print('Please revise your log txt!')
                print('------------------------------------------------')
                flag=input('input [Y]/N to continue\n');rewind=''
            else:
                print('------------------------------------------------')
                flag=input('please input [Y]/N to continue\n');rewind=''
    return



Path_Folder_script='/home/wqs/IRAF/rfscript/'          #the folder containing the suppied files
Path_Folder_Data='/home/wqs/IRAF/spectrum/'            #the folder containing the data folder

Gain=1.41;Ron=4.64
i=0;Path_Folder_Obj=Path_Folder_Data+os.listdir(Path_Folder_Data)[i]      #find the name of the first folder
os.chdir(Path_Folder_Obj);os.system('cd'+Path_Folder_Obj)                 #enter the first folder

OBS_DATE=os.listdir(Path_Folder_Data)[i]
PATH_log=Path_Folder_Obj+'/'+os.listdir(Path_Folder_Data)[i]+'.txt'

check_log(PATH_log,OBS_DATE,Path_Folder_script)

with open(PATH_log,'r') as f:
    txt_log=f.readlines();f.close()

inf_file=[];                                            #contaning regularized list of information of files
for j in range(len(txt_log)):      
        if OBS_DATE == txt_log[j][:8]:   #search for list of information of files
            inf_file.append([])                     
            inf_file[-1]=txt_log[j].split()
            if len(inf_file[-1])==4:                                               #bias                
                inf_file[-1]=inf_file[-1][:4]+[' ',' ',' ',' ',' ']
                expand_inf_file(inf_file)
                continue
            elif len(inf_file[-1])==6:                                             #flat/FeAr
                inf_file[-1]=inf_file[-1][:4]+[' ',' ',' ']+inf_file[-1][4:]
                expand_inf_file(inf_file)
                continue
            elif len(inf_file[-1])==9:                                             #object/companion
                expand_inf_file(inf_file)
                continue
            else:
                print('ERROE:Log Format Error!',j)

#make headers to match the instrunment 
for j in range(len(inf_file)):
        inf_file[j][1]=inf_file[j][1].replace('/','')
        iraf.hedit(inf_file[j][0],'OBJECT',inf_file[j][1],add=1,ver=0,up=1)
        iraf.hedit(inf_file[j][0],'Filter',inf_file[j][-2].replace('.','-'),add=1,ver=0,up=1)
        iraf.hedit(inf_file[j][0],'rdnoise',str(Ron),add=1,ver=0,up=1)
        iraf.hedit(inf_file[j][0],'gain',str(Gain),add=1,ver=0,up=1)
        iraf.hedit(inf_file[j][0],'dispaxis',1,add=1,ver=0,up=1)  #not usee for response
        if inf_file[j][1].lower() in ['bias']:
            inf_file[j][1]=inf_file[j][1].lower()
            iraf.hedit(inf_file[j][0],'IMAGETYP','BIAS',add=1,ver=0,up=1)   
        elif inf_file[j][1].lower() in ['flat']:
            inf_file[j][1]=inf_file[j][1].lower()
            iraf.hedit(inf_file[j][0],'IMAGETYP','DOME FLAT',add=1,ver=0,up=1)
        elif inf_file[j][1].lower() in ['skyflat']:
            inf_file[j][1]=inf_file[j][1].lower()
            iraf.hedit(inf_file[j][0],'IMAGETYP','SKY FLAT',add=1,ver=0,up=1)
        elif inf_file[j][1].lower() in ['fear']:
            iraf.hedit(inf_file[j][0],'IMAGETYP','OBJECT',add=1,ver=0,up=1)
        else:
            iraf.hedit(inf_file[j][0],'IMAGETYP','OBJECT',add=1,ver=0,up=1)
            iraf.hedit(inf_file[j][0],'RA',str(inf_file[j][4]),add=1,ver=0,up=1)
            iraf.hedit(inf_file[j][0],'DEC',str(inf_file[j][5].replace('+','')),add=1,ver=0,up=1)
            iraf.hedit(inf_file[j][0],'RA',str(inf_file[j][4]),add=1,ver=0,up=1)
            iraf.hedit(inf_file[j][0],'DEC',str(inf_file[j][5].replace('+','')),add=1,ver=0,up=1)

for j in range(len(inf_file)):
    newname=inf_file[j][0][0:8]+inf_file[j][1]+inf_file[j][0][8:]
    iraf.rename(Path_Folder_Obj+'/'+inf_file[j][0],Path_Folder_Obj+'/'+newname)
    inf_file[j][0]=newname

#zerocorretion and flatcombine
iraf.images.immatch();iraf.noao.imred();iraf.noao.imred.ccdred();iraf.unlearn('ccdproc');
write_files2file('fitlist','.fit');
iraf.noao.imred.ccdred(instrument='ccddb$kpno/specphot.dat')
iraf.noao.imred.ccdred.ccdproc('@fitlist',ccdtype='',fixpix=0,overscan=0,trim=1,zerocor=0,darkcor=0,flatcor=0,trimsec='[20:2020,400:1600]',zero='Zero')

bias_list=[inf_file[j][0] for j in range(len(inf_file)) if inf_file[j][1].lower() == 'bias'];write_list2file('biaslist',bias_list)
iraf.images.immatch.imcomb('@biaslist',output='Zero',rdnoise=Ron,gain=Gain)

iraf.noao.imred.ccdred.ccdproc('@fitlist',ccdtype='',fixpix=0,overscan=0,trim=1,zerocor=1,darkcor=0,flatcor=0,trimsec='[20:2020,400:1600]',zero='Zero')

flat_list=[inf_file[j][0] for j in range(len(inf_file)) if inf_file[j][1].lower() == 'flat'];write_list2file('flatlist',flat_list)
iraf.images.immatch.imcomb('@flatlist',output='Flat',rdnoise=Ron,gain=Gain)


#flatcorrection
iraf.noao.twod();iraf.noao.twodspec.longslit()
file_flat=find_files(Path_Folder_Obj,'Flat',flag=0)
for j in range(len(file_flat)):
    iraf.noao.twodspec.longslit.response(file_flat[j],file_flat[j],'re'+file_flat[j],interactive=0,func='chebyshev',o=8)
    iraf.noao.twodspec.longslit.illumination('re'+file_flat[j],'il'+file_flat[j],interactive=0,nbins=1,func='chebyshev',o=1)
    iraf.imarith('re'+file_flat[j],'*','il'+file_flat[j],'pf'+file_flat[j])

iraf.image.imutil();
iraf.image.imutil.imdel('Flat*fits,re*.fits,il*.fits,Zero*','yes',ver=0)
inf_file=reflesh(inf_file,'bias',1);inf_file=reflesh(inf_file,'flat',1);
write_files2file('fitandfits','.fit,.fits')
iraf.noao.imred.ccdred.ccdproc('@fitandfits',fixpix=0,overscan=0,trim=1,zerocor=1,darkcor=0,flatcor=1)

iraf.stsdas();iraf.unlearn('lacos_im');
image_spectrum=[inf_file[j][0] for j in range(len(inf_file)) if inf_file[j][-1] in ['o','c']]
[iraf.lacos_im(image_spectrum[j],image_spectrum[j].replace('.fit','_clean.fit'),image_spectrum[j].replace('.fit','.pl'),gain=Gain,readn=Ron,niter=3) for j in range(len(image_spectrum))]
pl_files=find_files(Path_Folder_Obj,'.pl');[os.remove(pl_files[j]) for j in range(len(pl_files))];
[os.remove(image_spectrum[j]) for j in range(len(image_spectrum))]
[iraf.imcopy(image_spectrum[j].replace('.fit','_clean.fit'),image_spectrum[j]) for j in range(len(image_spectrum))]
clean_files=find_files(Path_Folder_Obj,'_clean.fit');[os.remove(clean_files[j]) for j in range(len(clean_files))];
fits_file=find_files(Path_Folder_Obj,'.fits');[os.remove(fits_file[j]) for j in range(len(fits_file))];
lacos_file=find_files(Path_Folder_Obj,'lacos',flag=0);[os.remove(lacos_file[j]) for j in range(len(lacos_file))];

#use apall extract spectrum (flag: o,c)
iraf.noao.twodspec.apex();iraf.unlearn('apall');
image_spectrum=[inf_file[j][0] for j in range(len(inf_file)) if inf_file[j][-1] in ['o','c']]
iraf.image.imutil.imdel('*.ms.fits',ver=0)

#apall_upper=float(input('Upper aperture limit relative to center:\n'))
#apall_b_upper=float(input('Upper background limit relative to center:\n'))

apall_upper=20
apall_b_upper=60

apall_lower=-1*apall_upper
apall_b_sample=str(-1*apall_b_upper)+':'+str(apall_lower)+','+str(apall_upper)+':'+str(apall_b_upper)

[iraf.twodspec.apex.apall(image_spectrum[j],1,output=image_spectrum[j].replace('.fit','.ms.fits'),format='multispec',inter=0,lower=apall_lower,upper=apall_upper,b_sample=apall_b_sample,b_nave=-1000,t_func='legendre',t_order=5,back='fit') for j in range(len(image_spectrum))]

rewind=''
while rewind !='w':
    try:
        rewind='w'
        iraf.noao.twodspec.longslit.splot('*ms.fits');  #remove cosmic rays
        continueword = input('Are you sure have finished replacing files contaning cosmic-ray with new files? Input \'Y\' to continue.');
        if continueword.lower() == 'y':
            break
        else:
            rewind=''
            continue
    except:
        continueword = input('Are you sure have finished replacing files contaning cosmic-ray with new files? Input \'Y\' to continue.');
        if continueword.lower() == 'y':
            break
        else:
            rewind=''
            continue


#wavelength calibration
ms_files=find_files(Path_Folder_Obj,'ms.fits');ms_files=sorted(ms_files)
light_files=[inf_file[j][0] for j in range(len(inf_file)) if inf_file[j][-1]==('a')]
subsect_ms_files=[];subsect_light_files=[]
for ms_file in ms_files:
    subsect_ms_files.append([inf_file[j][-2] for j in range(len(inf_file)) if ms_file[:-7]+'fit' == inf_file[j][0]][0])

for light in light_files:
    subsect_light_files.append([inf_file[j][-2] for j in range(len(inf_file)) if light == inf_file[j][0]][0])

list_subsect=[]      #spectra classified in according to filters and the last term of every list is the FeAr spectrum image 
for j in range(len(light_files)):
    list_subsect.append([])
    list_subsect[-1]=[ms_files[k].replace('.ms.fits','.fit') for k in range(len(ms_files)) if subsect_ms_files[k]==subsect_light_files[j]]+[light_files[j]]
    [iraf.noao.twod.apex.apall(list_subsect[-1][-1],out=list_subsect[-1][k].replace('.fit','_lp.fits'),ref=list_subsect[-1][k],recen=0,trace=0,back='none',intera=0) for k in range(len(list_subsect[-1])-1)]

lamp_files=find_files(Path_Folder_Obj,'_lp.fits');lamp_files=sorted(lamp_files)
shutil.copy(Path_Folder_script+'wave_identify_lp.fits',Path_Folder_Obj)
shutil.copy(Path_Folder_script+'idwave_identify_lp',Path_Folder_Obj+'/database')


#interactively adjust parameter
#--------------------------------------------------------------------------------------------------------
#id_num=int(len(lamp_files)/2)
#identify_fwidth=12
#iraf.noao.twod.identify(lamp_files[id_num],coord='linelists$fear.dat',match=10,fwidth=identify_fwidth,nite=1)
#--------------------------------------------------------------------------------------------------------

iraf.noao.imred.kpnoslit();
[iraf.noao.imred.kpnoslit.reidentify('wave_identify_lp.fits',lamp_files[j],inter='NO',coord='linelists$fear.dat',match=10,nlost=0) for j in range(len(lamp_files))]

for j in range(len(lamp_files)):
    iraf.hedit(ms_files[j],'refspec1',lamp_files[j],add=1,ver=0,show=1)

write_files2file('mslist','ms.fits')
iraf.noao.imred.kpnoslit.dispcor('@mslist','dp_//@mslist',glob=0,confirm=0,listonly=0) #glob=1




#match the object stars with standard stars in according to their diatance 
object_files=[inf_file[j][0] for j in range(len(inf_file)) if inf_file[j][-1] in ['o']]

stand_names=[inf_file[j][1] for j in range(len(inf_file)) if inf_file[j][-1] in ['c']]
if stand_names!=[]:
    x_object=[inf_file[j][4] for j in range(len(inf_file)) if inf_file[j][-1] in ['o']]
    y_object=[inf_file[j][5] for j in range(len(inf_file)) if inf_file[j][-1] in ['o']]
    stand_files=[inf_file[j][0] for j in range(len(inf_file)) if inf_file[j][-1] in ['c']]
    x_standard=[inf_file[j][4] for j in range(len(inf_file)) if inf_file[j][-1] in ['c']]
    y_standard=[inf_file[j][5] for j in range(len(inf_file)) if inf_file[j][-1] in ['c']]
    distance_matrix=np.zeros((len(object_files),len(stand_files)));stand_object=[]
    for j in range(len(object_files)):
        for k in range(len(stand_files)):
            distance_matrix[j][k]=distance_points(x_object[j],y_object[j],x_standard[k],y_standard[k])
        distance_list=list(distance_matrix[j][:])
        stand_object.append(stand_files[distance_list.index(min(distance_list))])
    #write cmds files for prepare to calculate airmass
    with open("cmds",'w') as f:
        cmds_txt="observat = 'Bao'\nmst = mst (@'date-obs', obsdb (observat, 'longitude'))\nairmass = eairmass (ra, dec, mst, exptime, obsdb (observat, 'latitude'))"
        f.write(cmds_txt);f.close();
    dp_files=find_files(Path_Folder_Obj,'dp_',flag=0);
    [iraf.noao.astutil.asthedit(dp_files[j]+'[0]','cmds') for j in range(len(dp_files))]
    iraf.unlearn('standard');iraf.unlearn('sensfunc');iraf.unlearn('calibrate');
    [iraf.noao.imred.kpnoslit.standard('dp_'+stand_files[j][:-4]+'.ms.fits[0]',stand_files[j][:-4]+'_std',stand_names[j].lower(),extinct=Path_Folder_script+'baoextinct.dat',caldir=find_stand_path(stand_names[j],Path_Folder_script),observa='bao',interact='no') for j in range(len(stand_names))]
    [iraf.noao.imred.kpnoslit.sensfunc(stand_files[j][:-4]+'_std',stand_files[j][:-4]+'_sens',extinct=Path_Folder_script+'baoextinct.dat',observa='bao',order=2,funct='spline3',interact='no') for j in range(len(stand_names))]
    [iraf.noao.imred.kpnoslit.calibrate('dp_'+object_files[j][:-4]+'.ms.fits[0]',object_files[j][:-4]+'_ca.fits',sensiti=stand_object[j][:-4]+'_sens',extinct='yes',extinction=Path_Folder_script+'baoextinct.dat',observa='bao') for j in range(len(object_files))]

iraf.unlearn('continuum');
[iraf.noao.imred.kpnoslit.continuum('dp_'+object_files[j][:-4]+'.ms.fits[0]',object_files[j][:-4]+'_co.fits',interact='no',low_reject = 2,high_reject = 2,niterate = 10,order=6,func='spline3') for j in range(len(object_files))]
















