# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 14:32:22 2019

@author: c30557
"""

import predict_tools
#pdf to sentences
input_pdf='C:/Users/c30557/Desktop/predicttest/20190730_GRG_blank.pdf'
txt_sentence_dir='C:/Users/c30557/Desktop/predicttest/predict_input/test/neg/'

predict_tools.pdftosentence(input_pdf,txt_sentence_dir)


#tsv to out_pdf
tsv='C:/Users/c30557/Desktop/predicttest/transcript_classification.tsv'
outdoc='C:/Users/c30557/Desktop/predicttest/GRG_predict.pdf'

predict_tools.addhighlight_3class(input_pdf,outdoc,predict_tools.tsvtolist_3class(tsv,txt_sentence_dir))


'''
l=predict_tools.tsvtolist(tsv,txt_sentence_dir)
orderd_list=predict_tools.tsvtolist_3class(tsv,txt_sentence_dir)


with f=open('out.txt','rb'):
    f.write(orderd_list)
'''