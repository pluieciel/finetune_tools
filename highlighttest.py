# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 14:06:17 2019

@author: c30557
"""

import fitz
doc = fitz.open('C:/Users/c30557/Desktop/predicttest/20190222_SOP_blank.pdf')
for page in doc:
    #neg red
    for text,_ in l:
        text_instances = page.searchFor(text)
        ### HIGHLIGHT
        #color=round(1-confidence,2)
        for inst in text_instances:
            highlight = page.addHighlightAnnot(inst)
            highlight.setColors({"stroke":(1, 0.33, 0)})
            highlight.update() 




### OUTPUT
doc.save('C:/Users/c30557/Desktop/predicttest/SOP_111.pdf', garbage=4, deflate=True, clean=True)




text_instances = page.searchFor("<Q>: Thank you.")
text_instances


alll=page.getTextWords()
for i in alll:
    if i[4]=="<Q>:":
        print(i)