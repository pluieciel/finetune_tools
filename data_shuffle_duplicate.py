# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 10:35:28 2019

@author: c30557
"""
import os, shutil, math, re
import numpy as np

def shuffle_duplicate(data_dir='C:/Users/c30557/Desktop/data ready to use/',source_dir='C:/Users/c30557/Desktop/done data with labels/'):
    #data_dir='C:/Users/c30557/Desktop/data with labels/'
    os.mkdir(data_dir+'data')
    os.mkdir(data_dir+'data/train')
    os.mkdir(data_dir+'data/train/other')
    
    for dir_test in ['data_t_p','data_t_n','data_t_y','data_t_o']:
        os.mkdir(data_dir+dir_test)
        os.mkdir(data_dir+dir_test+'/test')
        for dir_under in ['pos','neg','yellow','other']:
            os.mkdir(data_dir+dir_test+'/test/'+dir_under)
       
    
    shutil.copytree(source_dir+r'yellow',data_dir+'data/train/yellow')
    shutil.copytree(source_dir+r'pos',data_dir+'data/train/pos')
    shutil.copytree(source_dir+r'neg',data_dir+'data/train/neg')
    _,_,f_y = next(os.walk(data_dir+'data/train/yellow'))
    ynum=len(f_y)
    print (ynum)
    _,_,f_p = next(os.walk(data_dir+'data/train/pos'))
    pnum=len(f_p)
    print (pnum)
    _,_,f_n = next(os.walk(data_dir+'data/train/neg'))
    nnum=len(f_n)
    print (nnum)
    
    #other too much, get from "done/other"
    _,_,f_other = next(os.walk(source_dir+'other'))
    other_num_raw=len(f_other)
    print (other_num_raw)
    testidx=np.random.permutation(other_num_raw)[0:ynum]
    for idx in testidx:
        shutil.copy(source_dir+'other/'+f_other[idx], data_dir+'data/train/other/'+f_other[idx])
    
    
    for cl in ['pos','neg','yellow', 'other']:
        path=data_dir+'data/train/'+cl+'/'
        outpath=data_dir+{'pos':'data_t_p','neg':'data_t_n','yellow':'data_t_y', 'other':'data_t_o'}[cl]+'/test/'+cl+'/'
        
        f = [f for _,_,f in os.walk(path)][0]
        print (len(f))
        #    for file in f:
        r=0.15
        testidx=np.random.permutation(len(f))[0:int(len(f)*r)]
        
        for idx in testidx:
            shutil.move(path+f[idx], outpath+f[idx])
    

    for j,cl in enumerate(['pos','neg']):        
        path=data_dir+'data/train/'+cl+'/'
        outpath=data_dir+'data/train/'+cl+'/'
        f = [f for _,_,f in os.walk(path)][0]
        print (len(f))
        for ff in f:
            for i in range(math.round(ynum/[pnum,nnum][j])-1):
            #for i in range(1):
                shutil.copy(path+ff, outpath+str(i)+re.findall(r'.+(?=.txt)',ff)[0]+'.txt')
    
    print('finished!')
                
shuffle_duplicate()