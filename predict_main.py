# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 14:32:22 2019

@author: c30557
"""
'''
phase=0
'''
#phase=1
#import re
import predict_tools,shutil,os

input_dir='C:/Users/c30557/Desktop/predicttest/'
txt_sentence_dir='C:/Users/c30557/Desktop/predicttest/predict_input/test/neg/'

r, d, f = next(os.walk(input_dir))
doc_list=[file for file in f if file.rfind('.pdf') != -1]

shutil.rmtree(txt_sentence_dir)
os.mkdir(txt_sentence_dir)

for num, doc in enumerate(doc_list):
    input_pdf='C:/Users/c30557/Desktop/predicttest/'+doc
    predict_tools.pdftosentence(input_pdf,txt_sentence_dir,num)







###################################################################################################################


