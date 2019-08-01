# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 10:17:49 2019

@author: c30557
"""
import os
import numpy as np
import shutil

if os.path.isdir('C:/Users/c30557/Desktop/data with labels/data/test/pos'):
    pass
else:
    os.mkdir('C:/Users/c30557/Desktop/data with labels/data/test')
    os.mkdir('C:/Users/c30557/Desktop/data with labels/data/test/pos')
    os.mkdir('C:/Users/c30557/Desktop/data with labels/data/test/neg')
    os.mkdir('C:/Users/c30557/Desktop/data with labels/data/test/other')



for cl in ['pos','neg','other']:
    path='C:/Users/c30557/Desktop/data with labels/data/train/'+cl+'/'
    outpath='C:/Users/c30557/Desktop/data with labels/data/test/'+cl+'/'
    
    f = [f for _,_,f in os.walk(path)][0]
    print (len(f))
    #    for file in f:
    r=0.15
    testidx=np.random.permutation(len(f))[0:int(len(f)*r)]
    
    for idx in testidx:
        shutil.move(path+f[idx], outpath+f[idx])


'''
import re
path='C:/Users/c30557/Desktop/data with labels/data/train/pos/'
outpath='C:/Users/c30557/Desktop/data with labels/data/train/pos/'
f = [f for _,_,f in os.walk(path)][0]
print (len(f))
for ff in f:
    shutil.copy(path+ff, outpath+'n'+re.findall(r'.+(?=.txt)',ff)[0]+'.txt')
'''
'''
import re
path='C:/Users/c30557/Desktop/data with labels/other1/'
outpath='C:/Users/c30557/Desktop/data with labels/other/'
f = [f for _,_,f in os.walk(path)][0]
print (len(f))
testidx=np.random.permutation(len(f))[0:1299]
for idx in testidx:
    shutil.move(path+f[idx], outpath+f[idx])
'''