# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 14:26:03 2019

@author: c30557

text_path = r'C:/Users/c30557/Desktop/predicttest/20190725_MTX-EarningsCall-vuDK.pdf'
out_path = r'C:/Users/c30557/Desktop/predicttest/predict/'
pdftosentence(text_path, out_path)
addhighlight(indoc,pos_list,neg_list,outdoc)
tsv='C:/Users/c30557/Desktop/predicttest/imdb.tsv'
predict_sentence_dir='C:/Users/c30557/Desktop/predicttest/predict/'
indoc='C:/Users/c30557/Desktop/predicttest/20190725_MTX_blank.pdf'
outdoc='C:/Users/c30557/Desktop/predicttest/out.pdf'
"""

import fitz
import csv
import re
import shutil,os
import numpy as np
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO

import os
import numpy as np
import shutil
import math

def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text



def pdftosentence(indoc,outdir,indocindex=0):
    #shutil.rmtree(outdir)
    #os.mkdir(outdir)
    
    txt=convert_pdf_to_txt(indoc)
    
    txt=re.sub(r'\n',' ',txt)
    txt=re.sub(r'Company Name:.+?\x0c',' ',txt,flags=re.S)
    
    pattern = re.compile(r'.+?(?<!Mr)(?<!Mrs)(?<!Ms)(?<!\.[^.])(?<![^.]\.)[.!?](?!.\.)(?!com)(?!\d)',re.S)
    sen = pattern.findall(txt)
    for i,s in enumerate(sen):
        #print('*',[s.strip()])
        if i==0:continue
        if s.strip() in ['Yes.','yes.','No.','Thank you.','.']:continue
        elif len(s.strip().split())<4 :continue
        f=open(outdir+str(indocindex)+'_'+str(i)+'.txt','wb')
        f.write(s.strip().encode('utf8'))
        f.close()
    
    



def softmax(x):
    """Compute softmax values for each sets of scores in x."""
    return np.round(np.exp(x) / np.sum(np.exp(x), axis=0),4)



def tsvtolist_2class(tsv,predict_sentence_dir):
    with open(tsv) as tsvfile:
        tsvreader = csv.reader(tsvfile, delimiter="\t")
        list1=list()
        for line in tsvreader:
            list1.append(line)
    list1=list1[1:]
    for i in list1:
        i[1]=[j for j in map(float,re.findall(r'-*\d+\.\d+e*-*\d*',i[1]))]
        i[1].append(softmax(i[1]))
        i[1].append(i[1][0]-i[1][1])
        with open(predict_sentence_dir+i[0]+'.txt',encoding='utf-8') as f:
            txt = f.read()
        i[0]=txt
    orderd_list=sorted(list1,key=lambda x:x[1][3])
    #[['txt'
    #   [logit_neg, logit_pos, array_softmax, neg-pos]
    #  ],
    #...]
    return orderd_list


### READ IN PDF
def addhighlight_2class(indoc,outdoc,orderd_list,pnum=0.15,nnum=0.05):
    doc = fitz.open(indoc)
    pos_list=orderd_list[0:round(len(orderd_list)*pnum-1)]
    neg_list=orderd_list[::-1][0:round(len(orderd_list)*nnum-1)]
    for page in doc:
        #pos green
        for text,_ in pos_list:
            text_instances = page.searchFor(text)
            ### HIGHLIGHT
            #color=round(1-confidence,2)
            for inst in text_instances:
                highlight = page.addHighlightAnnot(inst)
                highlight.setColors({"stroke":(0.75, 1, 0.75)})
                highlight.update() 
    for page in doc:
        #neg red
        for text,_ in neg_list:
            text_instances = page.searchFor(text)
            ### HIGHLIGHT
            #color=round(1-confidence,2)
            for inst in text_instances:
                highlight = page.addHighlightAnnot(inst)
                highlight.setColors({"stroke":(1, 0.33, 0)})
                highlight.update() 
    
    
    for page in doc:
        #add scores
        for text,score in orderd_list:
            text_instances = page.searchFor(text)
            ### scores 
            for inst in text_instances:
                confidence=page.addFreetextAnnot(inst,'p'+str(score[2][1]),8,)
                confidence.update(fontsize=6, text_color=[0,0,1], border_color=None, fill_color=None, rotate=-1)

    ### OUTPUT
    doc.save(outdoc, garbage=4, deflate=True, clean=True)
    

    
def tsvtolist_4class(tsv,predict_sentence_dir,num=0):
    with open(tsv) as tsvfile:
        tsvreader = csv.reader(tsvfile, delimiter="\t")
        list1=list()
        for line in tsvreader:
            list1.append(line)
    list1=list1[1:]
    orderd_list=[]
    for i in list1:
        if int(i[0])==num:
            with open(predict_sentence_dir+i[0]+'_'+i[1]+'.txt',encoding='utf-8') as f:
                txt = f.read()
            orderd_list.append([txt,[j for j in map(float,re.findall(r'-*\d+\.\d+e*[-+]*\d*',i[2]))]])
        #i[1]=[j for j in map(float,re.findall(r'-*\d+\.\d+e*[-+]*\d*',i[1]))]
        #i[1].append(softmax(i[1]))
        #i[1].append(i[1][0]-i[1][1])
            
    #orderd_list=sorted(list1,key=lambda x:x[1][5])
    #[['txt'
    #   [logit_neg, logit_pos, logit_yellow, logit_other, array_softmax, neg-pos]
    #  ],
    #...]
    return orderd_list


def addhighlight_4class(indoc,outdoc,orderd_list):
    doc = fitz.open(indoc)
    #pos_list=orderd_list[0:round(len(orderd_list)*pnum-1)]
    #neg_list=orderd_list[::-1][0:round(len(orderd_list)*nnum-1)]
    pos_list=list(filter(lambda x: x[1][1]==max(x[1]),orderd_list))
    neg_list=list(filter(lambda x: x[1][0]==max(x[1]),orderd_list))
    yellow_list=list(filter(lambda x: x[1][2]==max(x[1]),orderd_list))
    for page in doc:
        #pos green
        for text,_ in pos_list:
            text_instances = page.searchFor(text,quads=True)
            ### HIGHLIGHT
            #color=round(1-confidence,2)
            #for inst in text_instances:
            highlight = page.addHighlightAnnot(text_instances)
            highlight.setColors({"stroke":(0.75, 1, 0.75)})
            highlight.update() 
    for page in doc:
        #neg red
        for text,_ in neg_list:
            text_instances = page.searchFor(text,quads=True)
            ### HIGHLIGHT
            #color=round(1-confidence,2)
            #for inst in text_instances:
            highlight = page.addHighlightAnnot(text_instances)
            highlight.setColors({"stroke":(1, 0.33, 0)})
            highlight.update() 
    for page in doc:
        #yellow
        for text,_ in yellow_list:
            text_instances = page.searchFor(text,quads=True)
            ### HIGHLIGHT
            #color=round(1-confidence,2)
            #for inst in text_instances:
            highlight = page.addHighlightAnnot(text_instances)
            highlight.setColors({"stroke":(1, 1, 0)})
            highlight.update() 
    
    if 0:
        for page in doc:
            #add scores
            for text,score in orderd_list:
                text_instances = page.searchFor(text)
                ### scores 
                for inst in text_instances:
                    #print(score)
                    confidence=page.addFreetextAnnot(inst,'p'+str(round(score[1],2))+'n'+str(round(score[0],2))+'y'+str(round(score[2],2)),6,)
                    confidence.update(fontsize=6, text_color=[0.5,0.5,1], border_color=None, fill_color=None, rotate=-1)

    ### OUTPUT
    doc.save(outdoc, garbage=4, deflate=True, clean=True)
    doc.close()
    
    
    
    

                
def tsvtolist_3class(tsv,predict_sentence_dir,num=0):
    with open(tsv) as tsvfile:
        tsvreader = csv.reader(tsvfile, delimiter="\t")
        list1=list()
        for line in tsvreader:
            list1.append(line)
    list1=list1[1:]
    orderd_list=[]
    for i in list1:
        if int(i[0])==num:
            with open(predict_sentence_dir+i[0]+'_'+i[1]+'.txt',encoding='utf-8') as f:
                txt = f.read()
            orderd_list.append([txt,[j for j in map(float,re.findall(r'-*\d+\.\d+e*[-+]*\d*',i[2]))]])
        #i[1]=[j for j in map(float,re.findall(r'-*\d+\.\d+e*[-+]*\d*',i[1]))]
        #i[1].append(softmax(i[1]))
        #i[1].append(i[1][0]-i[1][1])
            
    #orderd_list=sorted(list1,key=lambda x:x[1][5])
    #[['txt'
    #   [logit_neg, logit_pos, logit_yellow, logit_other, array_softmax, neg-pos]
    #  ],
    #...]
    return orderd_list


def addhighlight_3class(indoc,outdoc,orderd_list):
    doc = fitz.open(indoc)
    #pos_list=orderd_list[0:round(len(orderd_list)*pnum-1)]
    #neg_list=orderd_list[::-1][0:round(len(orderd_list)*nnum-1)]
    pos_list=list(filter(lambda x: x[1][1]==max(x[1]),orderd_list))
    neg_list=list(filter(lambda x: x[1][0]==max(x[1]),orderd_list))
    #yellow_list=list(filter(lambda x: x[1][2]==max(x[1]),orderd_list))
    for page in doc:
        #pos green
        for text,_ in pos_list:
            text_instances = page.searchFor(text,quads=True)
            ### HIGHLIGHT
            #color=round(1-confidence,2)
            #for inst in text_instances:
            if text_instances:
                highlight = page.addHighlightAnnot(text_instances)
                highlight.setColors({"stroke":(0.75, 1, 0.75)})
                highlight.update() 
    for page in doc:
        #neg red
        for text,_ in neg_list:
            text_instances = page.searchFor(text,quads=True)
            ### HIGHLIGHT
            #color=round(1-confidence,2)
            #for inst in text_instances:
            if text_instances:
                highlight = page.addHighlightAnnot(text_instances)
                highlight.setColors({"stroke":(1, 0.33, 0)})
                highlight.update() 
    
    
    if 0:
        for page in doc:
            #add scores
            for text,score in orderd_list:
                text_instances = page.searchFor(text)
                ### scores 
                for inst in text_instances:
                    #print(score)
                    confidence=page.addFreetextAnnot(inst,'p'+str(round(score[1],2))+'n'+str(round(score[0],2))+'o'+str(round(score[2],2)),6,)
                    confidence.update(fontsize=6, text_color=[0.5,0.5,1], border_color=None, fill_color=None, rotate=-1)

    ### OUTPUT
    doc.save(outdoc, garbage=4, deflate=True, clean=True)
    doc.close()
              
                
                
                
                
                
                
                
                
                
                
                
                
                
                
