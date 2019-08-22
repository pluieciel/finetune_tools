# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 19:57:47 2019

@author: c30557
"""

#tsv to out_pdf
tsv='C:/Users/c30557/Desktop/predicttest/transcript_classification.tsv'
#outdoc=re.sub(r'blank',r'predict',input_pdf)

for num, doc in enumerate(doc_list):
    input_pdf='C:/Users/c30557/Desktop/predicttest/'+doc
    outdoc='C:/Users/c30557/Desktop/predicttest/'+doc[0:-4]+'_MH2.pdf'

    predict_tools.addhighlight_3class(input_pdf,outdoc,predict_tools.tsvtolist_3class(tsv,txt_sentence_dir,num))